#!/usr/bin/env python3
"""
Gmail Job Application Resender with Scheduling
Automatically resends job application emails from your sent folder with scheduling support
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta

import config
from gmail_service import GmailService
from message_handler import MessageHandler


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,  # Changed to DEBUG temporarily
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def load_excluded_emails():
    """Load excluded email addresses from file"""
    excluded_emails = set()
    if os.path.exists(config.EXCLUSION_FILE):
        try:
            with open(config.EXCLUSION_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    email = line.strip().lower()
                    if email and not email.startswith(
                        "#"
                    ):  # Skip empty lines and comments
                        excluded_emails.add(email)
            if excluded_emails:
                print(
                    f"Loaded {len(excluded_emails)} excluded email(s) from {config.EXCLUSION_FILE}"
                )
        except Exception as e:
            print(
                f"Warning: Could not read exclusion file {config.EXCLUSION_FILE}: {e}"
            )
    return excluded_emails


def add_to_exclusion_list(email):
    """Add an email address to the exclusion list file"""
    try:
        # Create file if it doesn't exist
        if not os.path.exists(config.EXCLUSION_FILE):
            with open(config.EXCLUSION_FILE, "w", encoding="utf-8") as f:
                f.write("# Email Exclusion List\n")
                f.write(
                    "# Add email addresses that you don't want to resend applications to\n"
                )
                f.write("# One email per line\n\n")

        # Check if email is already in the file
        with open(config.EXCLUSION_FILE, "r", encoding="utf-8") as f:
            content = f.read().lower()
            if email.lower() in content:
                print(f"Email {email} is already in the exclusion list")
                return

        # Add the email to the file
        with open(config.EXCLUSION_FILE, "a", encoding="utf-8") as f:
            f.write(f"{email.lower()}\n")
        print(f"Added {email} to exclusion list ({config.EXCLUSION_FILE})")

    except Exception as e:
        print(f"Error adding email to exclusion list: {e}")


def count_emails_to_recipient(gmail_service, recipient_email, logger):
    """Count how many emails have been sent to a specific recipient"""
    try:
        # Search for all emails sent to this recipient
        search_query = f"in:sent to:{recipient_email}"
        logger.debug(f"Counting emails sent to: {recipient_email}")

        messages = gmail_service.search_messages(search_query, max_results=100)
        count = len(messages) if messages else 0

        logger.debug(f"Found {count} emails previously sent to {recipient_email}")
        return count

    except Exception as e:
        logger.error(f"Error counting emails to {recipient_email}: {e}")
        return 0


def create_scheduled_task(scheduled_time):
    """Create a Windows Task Scheduler task to run the script at the specified time"""
    try:
        task_name = f"GmailResender_{scheduled_time.strftime('%Y%m%d_%H%M%S')}"
        script_path = os.path.abspath(__file__)

        # Create the schtasks command
        schtasks_cmd = [
            "schtasks",
            "/create",
            "/tn",
            task_name,
            "/tr",
            f'python "{script_path}" --execute-scheduled',
            "/st",
            scheduled_time.strftime("%H:%M"),
            "/sd",
            scheduled_time.strftime("%m/%d/%Y"),
            "/sc",
            "once",
            "/f",  # Force create (overwrite if exists)
        ]

        print(f"\n📅 Creating scheduled task: {task_name}")
        print(f"⏰ Scheduled for: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

        result = subprocess.run(
            schtasks_cmd, capture_output=True, text=True, shell=False
        )

        if result.returncode == 0:
            print(f"✅ Task scheduled successfully!")
            print(f"📝 Task name: {task_name}")
            print(f"\n💡 You can:")
            print(f"   • View tasks: schtasks /query /tn {task_name}")
            print(f"   • Delete task: schtasks /delete /tn {task_name} /f")
            print(f"\n🔔 The script will automatically run at the scheduled time.")
            print(f"📜 Check the log file for results: {config.LOG_FILE}")
            return True
        else:
            print(f"❌ Failed to create scheduled task:")
            print(f"Error: {result.stderr}")
            print(f"\n🔄 Falling back to immediate execution...")
            return False

    except Exception as e:
        print(f"❌ Error creating scheduled task: {e}")
        print(f"🔄 Falling back to immediate execution...")
        return False


def get_scheduled_time():
    """Get the scheduled time from user input"""
    print("\n" + "=" * 50)
    print("EMAIL PROCESSING OPTIONS")
    print("=" * 50)
    print("Choose how to handle emails:")
    print("1. Send immediately")
    print("2. Create drafts only (you'll schedule in Gmail)")
    print("3. Schedule delivery time (create drafts now, deliver later)")
    print("4. Schedule script execution time (run script later)")

    while True:
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            return (
                datetime.now(),
                False,
                "immediate",
            )  # Return (time, is_scheduled, method)

        elif choice == "2":
            return (
                datetime.now(),
                True,
                "create_drafts_only",
            )  # Create drafts without scheduling

        elif choice in ["3", "4"]:
            # Get the scheduled time
            print("\nChoose time option:")
            print("a. Specific time today")
            print("b. Specific date and time")

            while True:
                time_choice = input("Enter your choice (a/b): ").strip().lower()

                if time_choice == "a":
                    # Schedule for today
                    while True:
                        try:
                            time_str = input(
                                "Enter time (HH:MM format, 24-hour): "
                            ).strip()
                            hour, minute = map(int, time_str.split(":"))

                            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                                print("Invalid time! Please use HH:MM format (24-hour)")
                                continue

                            scheduled_time = datetime.now().replace(
                                hour=hour, minute=minute, second=0, microsecond=0
                            )

                            # If the time has already passed today, schedule for tomorrow
                            if scheduled_time <= datetime.now():
                                scheduled_time += timedelta(days=1)
                                print(
                                    f"Time has passed for today. Scheduling for tomorrow at {scheduled_time.strftime('%Y-%m-%d %H:%M')}"
                                )

                            method = (
                                "draft_delivery"
                                if choice == "3"
                                else "script_execution"
                            )
                            return scheduled_time, True, method

                        except ValueError:
                            print(
                                "Invalid format! Please use HH:MM format (e.g., 14:30)"
                            )

                elif time_choice == "b":
                    # Schedule for specific date and time
                    while True:
                        try:
                            date_str = input("Enter date (YYYY-MM-DD): ").strip()
                            time_str = input(
                                "Enter time (HH:MM format, 24-hour): "
                            ).strip()

                            year, month, day = map(int, date_str.split("-"))
                            hour, minute = map(int, time_str.split(":"))

                            scheduled_time = datetime(year, month, day, hour, minute)

                            if scheduled_time <= datetime.now():
                                print("Scheduled time must be in the future!")
                                continue

                            method = (
                                "draft_delivery"
                                if choice == "3"
                                else "script_execution"
                            )
                            return scheduled_time, True, method

                        except ValueError:
                            print(
                                "Invalid format! Please use YYYY-MM-DD for date and HH:MM for time"
                            )
                else:
                    print("Invalid choice! Please enter 'a' or 'b'")

        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4")


def wait_until_scheduled_time(scheduled_time):
    """Wait until the scheduled time to start sending emails"""
    current_time = datetime.now()

    if scheduled_time <= current_time:
        print("Scheduled time has already passed. Starting immediately.")
        return True

    time_diff = scheduled_time - current_time
    total_seconds = int(time_diff.total_seconds())

    print(f"\nEmails scheduled for: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Waiting {time_diff} until scheduled time...")
    print("Press Ctrl+C to cancel scheduling\n")

    try:
        # Show countdown for the first few minutes, then check every minute
        if total_seconds <= 300:  # 5 minutes or less
            for remaining in range(total_seconds, 0, -1):
                mins, secs = divmod(remaining, 60)
                print(f"\rStarting in: {mins:02d}:{secs:02d}", end="", flush=True)
                time.sleep(1)
        else:
            # For longer waits, check every minute
            while datetime.now() < scheduled_time:
                current = datetime.now()
                remaining = scheduled_time - current

                if remaining.total_seconds() <= 0:
                    break

                hours, remainder = divmod(int(remaining.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)

                print(
                    f"\rStarting in: {hours:02d}:{minutes:02d}:{seconds:02d}",
                    end="",
                    flush=True,
                )
                time.sleep(60)  # Check every minute

        print(f"\n\n🕒 Scheduled time reached! Starting email resend process...")
        print("=" * 50)

    except KeyboardInterrupt:
        print(f"\n\nScheduling cancelled by user.")
        return False

    return True


def process_emails_batch(
    gmail_service,
    message_handler,
    messages,
    excluded_emails,
    logger,
    scheduled_time=None,
    create_drafts_only=False,
):
    """Process emails in batch with optional scheduling

    Args:
        gmail_service: GmailService instance
        message_handler: MessageHandler instance
        messages: List of message IDs to process
        excluded_emails: Set of emails to exclude
        logger: Logger instance
        scheduled_time: Optional datetime for draft delivery scheduling
        create_drafts_only: If True, only create drafts without scheduling
    """
    resent_count = 0
    skipped_count = 0
    error_count = 0
    processed_recipients = set()

    for i, message_meta in enumerate(messages, 1):
        try:
            logger.info(f"Processing message {i}/{len(messages)}")
            full_message = gmail_service.get_message(message_meta["id"])
            if not full_message:
                logger.warning(f"Could not retrieve message {message_meta['id']}")
                error_count += 1
                continue

            message_data = message_handler.extract_message_data(full_message)
            if not message_data:
                logger.warning(
                    f"Could not extract data from message {message_meta['id']}"
                )
                error_count += 1
                continue

            if not message_handler.is_job_application(message_data):
                logger.info(
                    f"Message doesn't appear to be a job application, skipping: {message_data['subject']}"
                )
                skipped_count += 1
                continue

            if not message_handler.validate_email_address(message_data["to"]):
                logger.warning(f"Invalid recipient email address: {message_data['to']}")
                skipped_count += 1
                continue

            # Check if email is in exclusion list
            if message_data["to"].lower() in excluded_emails:
                logger.info(f"Email excluded from resending: {message_data['to']}")
                skipped_count += 1
                continue

            # Check if we've already sent too many emails to this recipient
            email_count = count_emails_to_recipient(
                gmail_service, message_data["to"], logger
            )
            if email_count >= config.MAX_EMAILS_PER_RECIPIENT:
                logger.info(
                    f"Already sent {email_count} emails to {message_data['to']} (limit: {config.MAX_EMAILS_PER_RECIPIENT}), skipping"
                )
                skipped_count += 1
                continue

            recipient_key = f"{message_data['to']}:{message_data['subject']}"
            if recipient_key in processed_recipients:
                logger.info(
                    f"Already processed this recipient/subject combination: {message_data['to']}"
                )
                skipped_count += 1
                continue

            processed_recipients.add(recipient_key)

            # Interactive mode: Ask user whether to resend this email
            if config.INTERACTIVE_MODE:
                print(f"\n{'='*60}")
                print(f"Email {i}/{len(messages)}")
                print(f"To: {message_data['to']}")
                print(f"Subject: {message_data['subject']}")
                print(f"Date: {message_data['date']}")
                print(f"{'='*60}")

                # Show a preview of the email body (first 200 characters)
                body_preview = (
                    message_data["body"][:200] + "..."
                    if len(message_data["body"]) > 200
                    else message_data["body"]
                )
                print(f"Body preview:\n{body_preview}\n")

                while True:
                    user_choice = (
                        input(
                            "Do you want to resend this email? (y/n/e to exclude permanently/q to quit): "
                        )
                        .lower()
                        .strip()
                    )
                    if user_choice in ["y", "yes"]:
                        break
                    elif user_choice in ["n", "no"]:
                        logger.info(
                            f"User chose to skip email to: {message_data['to']}"
                        )
                        skipped_count += 1
                        break
                    elif user_choice in ["e", "exclude"]:
                        # Add email to exclusion list and also to current set
                        add_to_exclusion_list(message_data["to"])
                        excluded_emails.add(message_data["to"].lower())
                        logger.info(
                            f"User chose to permanently exclude email: {message_data['to']}"
                        )
                        skipped_count += 1
                        break
                    elif user_choice in ["q", "quit"]:
                        logger.info("User chose to quit the application")
                        print(f"\nExiting... Processed {i-1} emails so far.")
                        return (
                            resent_count,
                            skipped_count,
                            error_count,
                            True,
                        )  # True indicates quit
                    else:
                        print(
                            "Please enter 'y' for yes, 'n' for no, 'e' to exclude permanently, or 'q' to quit."
                        )

                # If user chose 'n' or 'e', skip to next email
                if user_choice in ["n", "no", "e", "exclude"]:
                    continue

            logger.info(f"Resending application to: {message_data['to']}")
            logger.info(f"Subject: {message_data['subject']}")

            if not config.DRY_RUN:
                resend_message = message_handler.create_resend_message(message_data)
                if not resend_message:
                    logger.error(
                        f"Could not create resend message for {message_data['to']}"
                    )
                    error_count += 1
                    continue
                if create_drafts_only:
                    # Create draft only - user will schedule themselves
                    draft = gmail_service.create_draft(resend_message)
                    if draft:
                        logger.info(
                            f"Created draft for {message_data['to']} - you can schedule it in Gmail"
                        )
                    else:
                        logger.error(f"Failed to create draft for {message_data['to']}")
                        error_count += 1
                        continue
                elif scheduled_time:
                    # Create draft for scheduled delivery
                    gmail_service.send_scheduled_message(resend_message, scheduled_time)
                    logger.info(
                        f"Created draft for scheduled delivery at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                else:
                    # Send immediately
                    gmail_service.send_message(resend_message)
                resent_count += 1

                # Add recipient to exclusion list after successful send (if enabled)
                if config.AUTO_EXCLUDE_AFTER_SEND:
                    add_to_exclusion_list(message_data["to"])
                    excluded_emails.add(message_data["to"].lower())
                    if config.INTERACTIVE_MODE:
                        print(f"✓ Email sent successfully to {message_data['to']}")
                        print(f"✓ Added {message_data['to']} to exclusion list")
                    else:
                        logger.info(
                            f"Added {message_data['to']} to exclusion list after sending"
                        )
                else:
                    if config.INTERACTIVE_MODE:
                        print(f"✓ Email sent successfully to {message_data['to']}")

                if config.SEND_DELAY > 0:
                    logger.info(f"Waiting {config.SEND_DELAY} seconds...")
                    time.sleep(config.SEND_DELAY)
            else:
                logger.info("DRY RUN: Would resend message here")
                resent_count += 1
                if config.INTERACTIVE_MODE:
                    print(f"✓ DRY RUN: Would send email to {message_data['to']}")
                    if config.AUTO_EXCLUDE_AFTER_SEND:
                        print(
                            f"✓ DRY RUN: Would add {message_data['to']} to exclusion list"
                        )

        except Exception as e:
            logger.error(f"Error processing message {message_meta['id']}: {e}")
            error_count += 1
            continue

    return (
        resent_count,
        skipped_count,
        error_count,
        False,
    )  # False indicates normal completion


def main():
    """Main function with scheduling support"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Gmail Job Application Resender with Scheduling"
    )
    parser.add_argument(
        "--execute-scheduled",
        action="store_true",
        help="Execute scheduled email sending (used by Task Scheduler)",
    )
    args = parser.parse_args()

    logger = setup_logging()

    if args.execute_scheduled:
        # This is a scheduled execution, skip user interaction
        logger.info("Starting scheduled Gmail Job Application Resender")
        execute_email_resending(logger)
    else:
        # This is interactive mode with scheduling
        logger.info("Starting Gmail Job Application Resender with Scheduling")

        if config.DRY_RUN:
            logger.info("DRY RUN MODE - No emails will actually be sent")

        if False:  # Temporarily disable interactive mode
            logger.info(
                "INTERACTIVE MODE - You will be asked to confirm each email resend"
            )

        # Get scheduling preference from user
        scheduled_time, is_scheduled, method = get_scheduled_time()

        if is_scheduled:
            if method == "script_execution":
                # Traditional task scheduling - script runs later
                if create_scheduled_task(scheduled_time):
                    logger.info("Task scheduled successfully. Exiting...")
                    return
                else:
                    # Fall back to immediate execution if scheduling fails
                    logger.info("Scheduling failed, executing immediately...")
            elif method == "create_drafts_only":
                # Create drafts only - user will schedule themselves
                logger.info("Creating drafts only - you can schedule them in Gmail")
                execute_email_resending(logger, create_drafts_only=True)
                return
            elif method == "draft_delivery":
                # Create drafts now for delivery later
                logger.info(
                    f"Creating drafts for delivery at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                execute_email_resending(logger, scheduled_time=scheduled_time)
                return

        # Execute immediately (either chosen by user or fallback)
        execute_email_resending(logger)


def execute_email_resending(logger, scheduled_time=None, create_drafts_only=False):
    """Execute the email resending process

    Args:
        logger: Logger instance
        scheduled_time: Optional datetime for draft delivery scheduling
        create_drafts_only: If True, only create drafts without scheduling
    """
    # Load excluded emails
    excluded_emails = load_excluded_emails()

    try:
        gmail_service = GmailService()
        gmail_service.authenticate()
        message_handler = MessageHandler(gmail_service)
        keyword_query = " OR ".join([f'"{keyword}"' for keyword in config.JOB_KEYWORDS])
        search_query = f"in:sent ({keyword_query})"
        logger.info(f"Searching for sent emails with query: {search_query}")
        messages = gmail_service.search_messages(
            search_query, max_results=config.MAX_EMAILS_PER_RUN
        )

        if not messages:
            logger.info("No job application emails found in sent folder")
            return

        # Process emails in batch
        resent_count, skipped_count, error_count, user_quit = process_emails_batch(
            gmail_service,
            message_handler,
            messages,
            excluded_emails,
            logger,
            scheduled_time,
            create_drafts_only,
        )

        # Print summary (unless user quit early)
        if not user_quit:
            logger.info("\n" + "=" * 50)
            if create_drafts_only:
                logger.info("DRAFT CREATION SUMMARY")
            else:
                logger.info("RESEND SUMMARY")
            logger.info("=" * 50)
            logger.info(f"Total messages found: {len(messages)}")
            if create_drafts_only:
                logger.info(f"Drafts created: {resent_count}")
            else:
                logger.info(f"Messages resent: {resent_count}")
            logger.info(f"Messages skipped: {skipped_count}")
            logger.info(f"Errors encountered: {error_count}")

            if create_drafts_only:
                logger.info(f"\n✅ {resent_count} drafts created successfully!")
                logger.info("📧 Go to Gmail to schedule them for sending")
                logger.info(
                    "💡 In Gmail: Open draft → Click 'Send' dropdown → Choose 'Schedule send'"
                )
            elif config.DRY_RUN:
                logger.info("\nThis was a DRY RUN - no emails were actually sent")
                logger.info("Set DRY_RUN=False in .env to actually send emails")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

    logger.info("Gmail Job Application Resender completed")


if __name__ == "__main__":
    main()
