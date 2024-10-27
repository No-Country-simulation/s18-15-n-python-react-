import os
from dotenv  import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()

EMAIL_USER =  os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

email_reciber = "facundo.rua90@gmail.com"

subject = "Prueba"
body = "esto es una prueba"

em = EmailMessage()
em["From"] = "Planifica +"
em["To"] = email_reciber
em["Subject"] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as  smtp:
    smtp.login(EMAIL_USER, EMAIL_PASSWORD)
    smtp.sendmail(EMAIL_USER, email_reciber, em.as_string())






