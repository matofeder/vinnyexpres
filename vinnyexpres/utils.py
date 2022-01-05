import smtplib
import re
from dns import resolver
from email.message import EmailMessage

import config

EMAIL_TO = config.EMAIL_TO
EMAIL_FROM = config.EMAIL_FROM
EMAIL_FROM_PASS = config.EMAIL_FROM_PASS

# Simple Regex for email address syntax checking
EMAIL_REGEX = r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$"


class ValidateEmailError(Exception):
    """Email address validation error"""


def email_sent(content, email_to=", ".join(EMAIL_TO), subject="Vínny Expres Formulár"):
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = email_to
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_FROM_PASS)
        server.send_message(msg)


def email_validate(email_address):

    # Verify email address syntax
    if not re.match(EMAIL_REGEX, email_address):
        raise ValidateEmailError

    # MX record lookup
    user, domain = email_address.split("@")
    try:
        records = resolver.query(domain, "MX")
    except resolver.NXDOMAIN:
        raise ValidateEmailError

    # SMTP conversation
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    try:
        server.connect(str(records[0].exchange))
    except ConnectionRefusedError:
        raise ValidateEmailError

    server.helo(server.local_hostname)
    server.mail(EMAIL_FROM)
    code, message = server.rcpt(str(email_address))
    server.quit()

    # Assume SMTP response 250 is success
    if code != 250:
        raise ValidateEmailError
