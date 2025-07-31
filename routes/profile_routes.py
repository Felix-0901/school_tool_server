# routes/profile_routes.py

from flask import Blueprint, request, jsonify
from models import (
    db, User, Task, Diary, TimerRecord, Todo, Note
)
from sqlalchemy import and_

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/user', methods=['PUT'])
def update_profile():
    """
    PUT /user
    Body JSON: { "email": "...", "first_name": "...", "last_name": "..." }
    更新使用者的 First/Last name（email 不變）
    """
    data = request.get_json() or {}
    email = data.get('email')
    first = data.get('first_name')
    last = data.get('last_name')
    if not all([email, first, last]):
        return jsonify({'error': '缺少必要欄位'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': '使用者不存在'}), 404

    user.first_name = first
    user.last_name = last
    db.session.commit()
    return jsonify({'message': '更新成功'}), 200

@profile_bp.route('/user/password', methods=['PUT'])
def change_password():
    """
    PUT /user/password
    Body JSON: {
      "email": "...",
      "old_password": "...",
      "new_password": "...",
      "confirm_password": "..."
    }
    驗證舊密碼並更新為新密碼
    """
    data = request.get_json() or {}
    email = data.get('email')
    old = data.get('old_password')
    new = data.get('new_password')
    confirm = data.get('confirm_password')
    if not all([email, old, new, confirm]):
        return jsonify({'error': '缺少必要欄位'}), 400
    if new != confirm:
        return jsonify({'error': '新密碼與確認不符'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(old):
        return jsonify({'error': '舊密碼錯誤'}), 401

    user.set_password(new)
    db.session.commit()
    return jsonify({'message': '密碼已更新'}), 200

@profile_bp.route('/user', methods=['DELETE'])
def delete_account():
    """
    DELETE /user
    Body JSON: { "email": "..." }
    刪除該帳號及與其相關的所有資料
    """
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'error': '缺少 email'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': '使用者不存在'}), 404

    # 刪除所有 user_email 關聯的資料
    Task.query.filter_by(user_email=email).delete()
    Diary.query.filter_by(user_email=email).delete()
    TimerRecord.query.filter_by(email=email).delete()
    Todo.query.filter_by(user_email=email).delete()
    Note.query.filter_by(user_email=email).delete()

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '帳號及所有資料已刪除'}), 200
