# routes/announcement_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Announcement

announcement_bp = Blueprint('announcement', __name__)

@announcement_bp.route('/announcements', methods=['GET'])
def get_announcements():
    """
    取得最新 15 則公告，依 created_at DESC 排序
    """
    anns = Announcement.query.order_by(Announcement.created_at.desc()).limit(15).all()
    return jsonify([a.to_dict() for a in anns]), 200

@announcement_bp.route('/announcements', methods=['POST'])
def post_announcement():
    """
    新增一則公告（管理者使用）
    body JSON:
      {
        "title": "<標題>",
        "content": "<內文>"
      }
    """
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'Missing title or content'}), 400

    ann = Announcement(title=title, content=content)
    db.session.add(ann)
    db.session.commit()
    return jsonify({'message': 'Announcement created', 'id': ann.id}), 200
