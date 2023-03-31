import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import ssl
import email_constants

class email:
    sender_email = 'thomas.lemontagner@gmail.com'
    sender_password = email_constants.email_password
    receiver_email = 'thomas.le-montagner@hotmail.com'

    def send_email(self, subject, body):
        # Create a multipart message object and set its headers
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.receiver_email
        message['Subject'] = subject

        # Attach the body to the message
        message.attach(MIMEText(body, 'html'))

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())


    def send_intrusion_email(self, picture, date):
        subject = 'Intrusion Detected !'
        body = f'A intrusion has been detected. at {date} Please check'
        self.send_email(subject, body)




# Open the image file and attach it to the message
""" with open('path/to/image.jpg', 'rb') as image_file:
    image_data = image_file.read()
    image = MIMEImage(image_data, name='image.jpg')
    message.attach(image) """

