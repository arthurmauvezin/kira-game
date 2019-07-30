from typing import Optional
from datetime import datetime, timedelta

from core.config import config

import requests
import jwt
import logging
import json


def send_email(email_to: str, subject: str, template: str, variables={}):
    project_name = config['APP']['TITLE']
    domain_name = config['MAIL']['DOMAIN_NAME']
    subject = f"{project_name} - {subject}"

    result = requests.post(
        f"https://api.eu.mailgun.net/v3/{domain_name}/messages",
        auth=("api", config['MAIL']['API_KEY']),
        data={"from": f"{project_name} - No Reply <noreply@{domain_name}>",
                "to": [email_to],
                "subject": subject,
                "template": template,
                "h:X-Mailgun-Variables": json.dumps(variables) })

    logging.info(f"send email result: {result.json()}")


def send_test_email(email_to: str):
    subject = "Test email"
    variables = {
        "application": config['APP']['TITLE']
    }
    send_email(email_to=email_to, subject=subject, template="test_email", variables=variables)

def send_reset_password_email(email_to: str, username: str, token: str):

    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token

    subject = f"Password recovery for user {username}"
    server_host = config['APP']['SERVER_HOST']
    link = f"{server_host}/reset-password?token={use_token}"

    variables = {
        "project_name": config['APP']['TITLE'],
        "username": username,
        "email": email_to,
        "link": link,
        "valid_hours": config['MAIL']['RESET_TOKEN_EXPIRE_HOURS']
    }

    send_email(email_to=email_to, subject=subject, template="password_recovery", variables=variables)


def generate_password_reset_token(username):
    delta = timedelta(hours=int(config['MAIL']['RESET_TOKEN_EXPIRE_HOURS']))
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "sub": config['JWT']['PASSWORD_RESET_SUBJECT'],
            "username": username,
        },
        config['JWT']['SECRET_KEY'],
        algorithm=config['JWT']['ALGORITHM']
    )
    return encoded_jwt

def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, config['JWT']['SECRET_KEY'], algorithms=[config['JWT']['ALGORITHM']])
        assert decoded_token["sub"] == config['JWT']['PASSWORD_RESET_SUBJECT']
        return decoded_token["username"]
    except InvalidTokenError:
        return None
