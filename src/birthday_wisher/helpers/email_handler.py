import smtplib

from src.birthday_wisher.constants.constants import YOUR_EMAIL
from src.birthday_wisher.helpers.secret_manager import SecretManager

class EmailHandler:

    @staticmethod
    def send_birthday_emails(birthday_data, email_text):
        """Send birthday emails to the birthday person and CC Yourself"""
        try:
            # Get email credentials from SSM
            sender_email = SecretManager.get_secret('SENDER_EMAIL')
            email_password = SecretManager.get_secret('EMAIL_PASSWORD')

            with smtplib.SMTP("smtp.gmail.com") as connection:
                # Send to birthday person
                connection.starttls()
                connection.login(user=sender_email, password=email_password)

                # Send birthday wish
                connection.sendmail(
                    from_addr=sender_email,
                    to_addrs=birthday_data['email'],
                    msg=f"Subject:Happy Birthday!\n\n{email_text}"
                )

                # Send notification to Morgan
                connection.sendmail(
                    from_addr=sender_email,
                    to_addrs=YOUR_EMAIL,
                    msg=f"Subject:{birthday_data['name']}'s Birthday\n\n"
                        f"The bot has sent birthday wishes to {birthday_data['name']}. "
                        f"You may wish to consider sending something a little more personal with a text message."
                )

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
