# app.py

from flask import Flask
from flask_cors import CORS
from database import init_db, db
from dotenv import load_dotenv

# 把所有既有路由、以及新加的 timer_record Blueprint 都 import 進來
from routes import register_routes
from routes.timer_record import timer_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化 SQLAlchemy
init_db(app)

# 在 app context 內自動 create tables
with app.app_context():
    db.create_all()

# 註冊原本所有 Blueprint
register_routes(app)
# 註冊計時記錄的 Blueprint
app.register_blueprint(timer_bp)

if __name__ == "__main__":
    app.run(debug=True)
