from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config["DATABASE"] = 'database.db'

from app import views,models
