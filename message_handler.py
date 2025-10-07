import base64
import logging
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


class MessageHandler:
    def __init__(self, gmail_service):
        self.gmail_service = gmail_service
        self.logger = logging.getLogger(__name__)

    def clean_email(self, email):
        """Removes mailto, Markdown, brackets, and whitespace from an email string."""
        if not email:
            return ""
        # Remove Markdown hyperlinks: [text](mailto:email@example.com)
        mailto_match = re.search(
            r"mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})", email
        )
        if mailto_match:
            email = mailto_match.group(1)
        # Remove mailto: prefix if present
        if email.startswith("mailto:"):
            email = email[7:]
        # Remove brackets, extra symbols, whitespace
        email = email.strip("<>[]()").replace(" ", "").replace("\n", "")
        # Remove any lingering Markdown or URI artifacts
        email = email.replace("mailto:", "")
        return email

    def extract_message_data(self, message):
        """Extract relevant data from a Gmail message"""
        try:
            headers = {}
            for header in message["payload"]["headers"]:
                headers[header["name"].lower()] = header["value"]
            # Use clean_email on the TO field
            to_field = self.clean_email(headers.get("to", ""))
            return {
                "id": message["id"],
                "to": to_field,
                "subject": headers.get("subject", "(No Subject)"),
                "date": headers.get("date", ""),
                "body": self._extract_body(message["payload"]),
                "attachments": self._extract_attachments(
                    message["payload"], message["id"]
                ),
            }
        except Exception as e:
            self.logger.error(f"Error extracting message data: {e}")
            return None

    def _extract_body(self, payload):
        """Extract plain text body from message payload"""
        body = ""

        # Log payload structure for debugging
        self.logger.debug(f"Payload mimeType: {payload.get('mimeType', 'Unknown')}")
        self.logger.debug(f"Payload has parts: {'parts' in payload}")

        if "parts" in payload:
            for i, part in enumerate(payload["parts"]):
                self.logger.debug(
                    f"Part {i}: mimeType={part.get('mimeType', 'Unknown')}, has_data={'data' in part.get('body', {})}"
                )

                # Try plain text first
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8", errors="ignore"
                    )
                    self.logger.debug(
                        f"Extracted plain text body (length: {len(body)})"
                    )
                    break

                # If no plain text, try HTML and convert
                elif (
                    part["mimeType"] == "text/html"
                    and "data" in part["body"]
                    and not body
                ):
                    html_body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8", errors="ignore"
                    )
                    # Simple HTML to text conversion (remove tags)
                    body = re.sub(r"<[^>]+>", "", html_body)
                    body = re.sub(r"\s+", " ", body).strip()
                    self.logger.debug(
                        f"Extracted HTML body and converted to text (length: {len(body)})"
                    )

                # Handle nested multipart
                elif part["mimeType"].startswith("multipart/") and "parts" in part:
                    nested_body = self._extract_body(part)
                    if nested_body:
                        body = nested_body
                        self.logger.debug(
                            f"Extracted body from nested multipart (length: {len(body)})"
                        )
                        break

        elif payload["mimeType"] == "text/plain" and "data" in payload["body"]:
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode(
                "utf-8", errors="ignore"
            )
            self.logger.debug(f"Extracted simple plain text body (length: {len(body)})")

        elif payload["mimeType"] == "text/html" and "data" in payload["body"]:
            html_body = base64.urlsafe_b64decode(payload["body"]["data"]).decode(
                "utf-8", errors="ignore"
            )
            # Simple HTML to text conversion
            body = re.sub(r"<[^>]+>", "", html_body)
            body = re.sub(r"\s+", " ", body).strip()
            self.logger.debug(
                f"Extracted simple HTML body and converted to text (length: {len(body)})"
            )

        if not body:
            self.logger.warning("No body content extracted from message")

        return body

    def _extract_attachments(self, payload, message_id):
        """Extract attachment information from message payload"""
        attachments = []
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("filename"):
                    attachment_info = {
                        "filename": part["filename"],
                        "mime_type": part["mimeType"],
                        "attachment_id": part["body"].get("attachmentId"),
                        "message_id": message_id,
                    }
                    attachments.append(attachment_info)
        return attachments

    def create_resend_message(self, original_data):
        """Create a new message for resending"""
        try:
            # Create multipart message
            msg = MIMEMultipart()
            msg["To"] = original_data["to"]
            msg["Subject"] = f"{config.RESEND_PREFIX} {original_data['subject']}"

            # Debug logging
            self.logger.info(f"Creating resend message for: {original_data['to']}")
            self.logger.info(f"Original subject: {original_data['subject']}")
            self.logger.info(
                f"Original body length: {len(original_data.get('body', ''))}"
            )

            # Get original body and handle empty case
            original_body = original_data.get("body", "").strip()
            if not original_body:
                original_body = "[Original message content could not be extracted]"
                self.logger.warning(
                    f"Empty body for message to {original_data['to']}, using placeholder"
                )

            # Compose body with resend message
            full_body = config.RESEND_MESSAGE + original_body

            # Log the full body for debugging (first 200 chars)
            self.logger.debug(f"Full body preview: {full_body[:200]}...")

            msg.attach(MIMEText(full_body, "plain"))

            # Add attachments if any
            attachment_count = 0
            for attachment_info in original_data["attachments"]:
                if attachment_info["attachment_id"]:
                    attachment_data = self.gmail_service.get_attachment(
                        attachment_info["message_id"], attachment_info["attachment_id"]
                    )
                    if attachment_data:
                        file_data = base64.urlsafe_b64decode(attachment_data["data"])
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(file_data)
                        encoders.encode_base64(part)
                        filename = attachment_info["filename"]
                        part.add_header(
                            "Content-Disposition",
                            f'attachment; filename="{filename}"',
                        )
                        msg.attach(part)
                        attachment_count += 1
                        self.logger.debug(f"Added attachment: {filename}")

            self.logger.info(f"Created message with {attachment_count} attachments")

            # Convert to raw format for Gmail API
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
            return {"raw": raw_message}
        except Exception as e:
            self.logger.error(f"Error creating resend message: {e}")
            return None

    def is_job_application(self, message_data):
        subject = message_data["subject"].lower()
        body = message_data["body"].lower()
        for keyword in config.JOB_KEYWORDS:
            if keyword in subject or keyword in body:
                return True
        job_patterns = [
            "dear hiring manager",
            "dear recruiter",
            "i am writing to apply",
            "application for",
            "interested in the position",
            "attached resume",
            "cover letter",
        ]
        for pattern in job_patterns:
            if pattern in body:
                return True
        return False

    def validate_email_address(self, email):
        """Basic email validation with cleaning step included."""
        email = self.clean_email(email)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None
