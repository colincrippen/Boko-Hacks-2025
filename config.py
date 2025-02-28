import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///boko_hacks.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("GMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("GMAIL_USERNAME")
