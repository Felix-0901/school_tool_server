# lib/server/routes/timer_record.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, TimerRecord

timer_bp = Blueprint('timer', __name__)

@timer_bp.route('/record_timer', methods=['POST'])
def record_timer():
    data = request.get_json() or {}
    email   = data.get('email')
    date_str= data.get('date')      # 'YYYY-MM-DD'
    minutes = data.get('minutes')   # int
    mode    = data.get('mode')      # 'stopwatch'|'countdown'|'pomodoro'

    # 欄位檢查
    if not all([email, date_str, minutes is not None, mode]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        rec = TimerRecord(
            email=email,
            date=date_obj,
            minutes=int(minutes),
            mode=mode
        )
        db.session.add(rec)
        db.session.commit()
        return jsonify({'message': 'Recorded successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
