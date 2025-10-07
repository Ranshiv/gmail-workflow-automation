import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config


class GmailService:
    def __init__(self):
        self.service = None
        self.logger = logging.getLogger(__name__)

    def authenticate(self):
        creds = None
        if os.path.exists(config.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                config.TOKEN_FILE, config.SCOPES
            )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Refreshing expired token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(config.CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Credentials file not found at {config.CREDENTIALS_FILE}."
                    )
                self.logger.info("Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.CREDENTIALS_FILE, config.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(config.TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        self.service = build("gmail", "v1", credentials=creds)
        self.logger.info("Gmail service authenticated successfully")
        return self.service

    def search_messages(self, query, max_results=500):
        try:
            response = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )
            messages = response.get("messages", [])
            self.logger.info(f"Found {len(messages)} messages matching query: {query}")
            return messages
        except HttpError as error:
            self.logger.error(f"An error occurred while searching: {error}")
            return []

    def get_message(self, message_id):
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
            return message
        except HttpError as error:
            self.logger.error(
                f"An error occurred while getting message {message_id}: {error}"
            )
            return None

    def send_message(self, message_body):
        try:
            message = (
                self.service.users()
                .messages()
                .send(userId="me", body=message_body)
                .execute()
            )
            self.logger.info(f"Message sent successfully. ID: {message['id']}")
            return message
        except HttpError as error:
            self.logger.error(f"An error occurred while sending message: {error}")
            return None

    def send_scheduled_message(self, message_body, scheduled_time):
        """Create a draft for scheduled sending (to be sent later by task scheduler)"""
        try:
            # Create a draft first
            draft = self.create_draft(message_body)
            if not draft:
                return None

            self.logger.info(
                f"Draft created for scheduled delivery at {scheduled_time}"
            )
            return {
                "type": "scheduled_draft",
                "draft_id": draft["id"],
                "scheduled_time": scheduled_time,
                "message_id": draft.get("message", {}).get("id"),
            }

        except HttpError as error:
            self.logger.error(
                f"An error occurred while creating scheduled draft: {error}"
            )
            return None

    def send_draft(self, draft_id):
        """Send an existing draft"""
        try:
            message = (
                self.service.users()
                .drafts()
                .send(userId="me", body={"id": draft_id})
                .execute()
            )
            self.logger.info(f"Draft sent successfully. Message ID: {message['id']}")
            return message
        except HttpError as error:
            self.logger.error(
                f"An error occurred while sending draft {draft_id}: {error}"
            )
            return None

    def create_draft(self, message_body):
        """Create a draft message"""
        try:
            draft = (
                self.service.users()
                .drafts()
                .create(userId="me", body={"message": message_body})
                .execute()
            )
            self.logger.info(f"Draft created successfully. ID: {draft['id']}")
            return draft
        except HttpError as error:
            self.logger.error(f"An error occurred while creating draft: {error}")
            return None

    def get_attachment(self, message_id, attachment_id):
        """Get attachment data from a message"""
        try:
            attachment = (
                self.service.users()
                .messages()
                .attachments()
                .get(userId="me", messageId=message_id, id=attachment_id)
                .execute()
            )
            self.logger.info(
                f"Retrieved attachment {attachment_id} from message {message_id}"
            )
            return attachment
        except HttpError as error:
            self.logger.error(
                f"An error occurred while getting attachment {attachment_id}: {error}"
            )
            return None
