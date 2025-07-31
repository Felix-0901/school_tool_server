# app.py

from flask import Flask
from flask_cors import CORS
from database import init_db, db
from dotenv import load_dotenv

# 只要 import register_routes 即可，裡面會把所有 Blueprint 一次註冊完畢
from routes import register_routes

load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化資料庫設定
init_db(app)

# 在 app context 底下 create 所有 table（含新加的 todos、notes、timer_records、users、etc.）
with app.app_context():
    db.create_all()

# 註冊所有路由（包含 auth、task、diary、timer_record、study、user）
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
