from flask import Flask
from flask_cors import CORS
from database import init_db, db
from routes import register_routes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# 先初始化資料庫設定
init_db(app)

# 然後在 app context 下建立所有 table
with app.app_context():
    db.create_all()

# 最後註冊所有路由
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
