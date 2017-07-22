from flask import Flask
from passlib.context import CryptContext
from flask_restful import Api
import os

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(app.root_path, 'database.db')

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "des_crypt"],
    deprecated="auto",
)

from dabi import views,models
