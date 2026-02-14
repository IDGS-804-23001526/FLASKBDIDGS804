from re import DEBUG
import os

from sqlalchemy import create_engine

class Config():
    SECRET_KEY = "ClaveSecreta"
    SESSION_COOKIE_NAME = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Diego2495@localhost/bdidgs804'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    