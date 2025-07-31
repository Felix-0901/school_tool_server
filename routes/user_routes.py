# routes/user_routes.py

from flask import Blueprint, request, jsonify
from models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
def get_user():
    """
    GET /user?email=<email>
    回傳該 email 的使用者 first_name, last_name, email
    """
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Missing email parameter'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }), 200
