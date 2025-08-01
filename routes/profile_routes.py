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
    Update user's first and last name (email remains unchanged)
    """
    data = request.get_json() or {}
    email = data.get('email')
    first = data.get('first_name')
    last = data.get('last_name')
    if not all([email, first, last]):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.first_name = first
    user.last_name = last
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

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
    Verify old password and update to new password
    """
    data = request.get_json() or {}
    email = data.get('email')
    old = data.get('old_password')
    new = data.get('new_password')
    confirm = data.get('confirm_password')
    if not all([email, old, new, confirm]):
        return jsonify({'error': 'Missing required fields'}), 400
    if new != confirm:
        return jsonify({'error': 'New password and confirmation do not match'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(old):
        return jsonify({'error': 'Old password is incorrect'}), 401

    user.set_password(new)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200

@profile_bp.route('/user', methods=['DELETE'])
def delete_account():
    """
    DELETE /user
    Body JSON: { "email": "..." }
    Delete the account and all associated data
    """
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Delete all data related to this user
    Task.query.filter_by(user_email=email).delete()
    Diary.query.filter_by(user_email=email).delete()
    TimerRecord.query.filter_by(email=email).delete()
    Todo.query.filter_by(user_email=email).delete()
    Note.query.filter_by(user_email=email).delete()

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Account and all associated data have been deleted'}), 200
