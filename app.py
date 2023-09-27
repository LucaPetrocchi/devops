import os

import bcrypt

from flask import (
    Flask,
)
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
ma = Marshmallow(app)

from views.view import *

load_dotenv()

if __name__ == "__main__":
    app.run(port=5000, debug='True')