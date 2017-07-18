from flask import Flask
from flask_restful import Api
import os

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(app.root_path, 'database.db')
from app import views,models
