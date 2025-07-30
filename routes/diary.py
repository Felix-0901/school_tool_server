from flask import request, jsonify
from models import Diary
from database import db

def register_diary_routes(app):
    @app.route('/add_diary', methods=['POST'])
    def add_diary():
        data = request.get_json()
        email   = data.get('email')
        title   = data.get('title')
        date    = data.get('date')     # YYYY-MM-DD
        content = data.get('content')

        if not all([email, title, date]):
            return jsonify({'message': 'Missing required fields'}), 400

        new_diary = Diary(
            user_email=email,
            title=title,
            date=date,
            content=content or ''
        )
        db.session.add(new_diary)
        db.session.commit()
        return jsonify({'message': 'Diary added successfully'}), 200

    @app.route('/diaries', methods=['GET'])
    def get_diaries():
        email = request.args.get('email')
        month = request.args.get('month')  # 選填，格式 "YYYY-MM"
        if not email:
            return jsonify({'message': 'Email is required'}), 400

        query = Diary.query.filter_by(user_email=email)
        if month:
            # 只取當月日記
            query = query.filter(Diary.date.startswith(month))
        diaries = query.order_by(Diary.date).all()

        result = [{
            'id': d.id,
            'title': d.title,
            'date': d.date,
            'content': d.content
        } for d in diaries]

        return jsonify({'diaries': result}), 200

    @app.route('/update_diary/<int:diary_id>', methods=['PUT'])
    def update_diary(diary_id):
        data = request.get_json()
        d = Diary.query.get(diary_id)
        if not d:
            return jsonify({'message': 'Diary not found'}), 404

        d.title   = data.get('title', d.title)
        d.date    = data.get('date', d.date)
        d.content = data.get('content', d.content)
        db.session.commit()
        return jsonify({'message': 'Diary updated successfully'}), 200

    @app.route('/delete_diary/<int:diary_id>', methods=['DELETE'])
    def delete_diary(diary_id):
        d = Diary.query.get(diary_id)
        if not d:
            return jsonify({'message': 'Diary not found'}), 404

        db.session.delete(d)
        db.session.commit()
        return jsonify({'message': 'Diary deleted successfully'}), 200
