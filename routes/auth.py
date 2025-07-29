from flask import Blueprint, request, jsonify
from models import User
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("收到資料：", data)  # 可在 Render Logs 查看
    try:
        if not all(k in data for k in ("first_name", "last_name", "email", "password")):
            return jsonify({"message": "Missing fields"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email already exists"}), 400

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"]
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print("⚠️ 發生錯誤：", e)
        return jsonify({"message": "Server error"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        return jsonify({
            "message": "Login successful",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401
