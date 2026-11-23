import smtplib
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Send a test email via configured Django SMTP settings to verify Gmail delivery."

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            type=str,
            help='The recipient email address to receive the test message.'
        )

    def handle(self, *args, **options):
        recipient = options['recipient']
        
        self.stdout.write(self.style.NOTICE("--- Gmail SMTP Delivery Test ---"))
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST:    {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"SENDER USER:   {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"FROM HEADER:   {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"RECIPIENT:     {recipient}\n")
        self.stdout.write("Connecting to Gmail SMTP server and sending test email...")

        subject = "MyJournal - SMTP Configuration Test"
        message = (
            "Congratulations!\n\n"
            "This is a test message from your MyJournal Django application.\n"
            "Your Gmail SMTP connection is working properly.\n\n"
            "Your application is now ready to send real account verification "
            "and password recovery emails.\n\n"
            "— MyJournal Team"
        )

        try:
            sent_count = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            if sent_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n[SUCCESS] Test email successfully delivered to SMTP server for {recipient}!\n"
                        f"Check the recipient inbox (and spam folder) for the message."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING("\n[WARNING] send_mail returned 0 messages sent.")
                )

        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"\n[AUTHENTICATION ERROR] Gmail rejected the login credentials:\n"
                    f"Code: {e.smtp_code}, Message: {e.smtp_error.decode('utf-8', errors='ignore')}\n\n"
                    f"Troubleshooting:\n"
                    f"1. Make sure 2-Step Verification is active on '{settings.EMAIL_HOST_USER}'.\n"
                    f"2. Ensure the App Password in .env is 16 letters generated from Google Account Security."
                )
            )

        except (smtplib.SMTPConnectError, ConnectionRefusedError, TimeoutError, OSError) as e:
            self.stdout.write(
                self.style.ERROR(
                    f"\n[CONNECTION ERROR] Could not connect to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}:\n{e}\n\n"
                    f"Troubleshooting: Check internet connectivity and ensure port 587 is not blocked by a firewall."
                )
            )

        except smtplib.SMTPRecipientsRefused as e:
            self.stdout.write(
                self.style.ERROR(
                    f"\n[RECIPIENT REFUSED] Gmail rejected recipient '{recipient}':\n{e}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"\n[UNEXPECTED ERROR] {type(e).__name__}: {e}")
            )
