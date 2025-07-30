from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import register_routes
import os
from dotenv import load_dotenv
from models import Task
from database import db

load_dotenv()

app = Flask(__name__)
CORS(app)

init_db(app)
register_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
