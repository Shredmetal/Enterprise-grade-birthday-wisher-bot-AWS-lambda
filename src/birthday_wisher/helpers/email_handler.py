import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.birthday_wisher.constants.constants import BirthdayWishesConstants
from src.birthday_wisher.helpers.secret_manager import SecretManager


class EmailHandler:
    """
    Handles sending of birthday emails to the designated individuals and a
    notification email to the sender. The purpose of this class is to automate
    and streamline the process of sending birthday wishes while notifying the
    user about the action taken. It facilitates email creation and delivery using
    SMTP.

    """
    @staticmethod
    def send_birthday_emails(birthday_data, email_text) -> bool:
        """
        Sends birthday emails to the specified recipient with a dedicated birthday
        message and also a notification email to the configured email owner about
        the action. Utilizes email server credentials retrieved securely and ensures
        email delivery for both messages.

        :param birthday_data: A dictionary containing details of the person whose
            birthday it is. Key-value pairs include "name" (the name of the person)
            and "email" (the recipient's email address).
        :param email_text: The text content of the birthday email to be sent.
        :return: A boolean value indicating whether the emails were sent
            successfully or not.
        :rtype: bool
        """
        try:
            # Get email credentials from SSM
            sender_email = SecretManager.get_secret('SENDER_EMAIL')
            email_password = SecretManager.get_secret('EMAIL_PASSWORD')

            # Create birthday email
            birthday_msg = MIMEMultipart()
            birthday_msg['From'] = sender_email
            birthday_msg['To'] = birthday_data['email']
            birthday_msg['Subject'] = "Happy Birthday!"
            birthday_msg.attach(MIMEText(email_text, 'plain', 'utf-8'))

            # Create notification email
            notification_msg = MIMEMultipart()
            notification_msg['From'] = sender_email
            notification_msg['To'] = BirthdayWishesConstants.YOUR_EMAIL
            notification_msg['Subject'] = f"{birthday_data['name']}'s Birthday"
            notification_text = (
                f"The bot has sent birthday wishes to {birthday_data['name']}. "
                f"You may wish to consider sending something a little more personal with a text message."
            )
            notification_msg.attach(MIMEText(notification_text, 'plain', 'utf-8'))

            # Send emails
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(user=sender_email, password=email_password)

                # Send birthday wish
                server.send_message(birthday_msg)

                # Send notification
                server.send_message(notification_msg)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
