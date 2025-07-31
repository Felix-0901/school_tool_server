# lib/server/routes/timer_record.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, TimerRecord

timer_bp = Blueprint('timer', __name__)

def _record_to_dict(rec: TimerRecord):
    return {
        'id': rec.id,
        'email': rec.email,
        'date': rec.date.isoformat(),
        'minutes': rec.minutes,
        'mode': rec.mode,
        'created_at': rec.created_at.isoformat()
    }

@timer_bp.route('/record_timer', methods=['POST'])
def record_timer():
    data = request.get_json() or {}
    email    = data.get('email')
    date_str = data.get('date')      # 'YYYY-MM-DD'
    minutes  = data.get('minutes')   # int
    mode     = data.get('mode')      # 'stopwatch'|'countdown'|'pomodoro'

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

@timer_bp.route('/timer_records', methods=['GET'])
def get_timer_records():
    """
    Query params:
      email=<user_email>      (required)
      month=YYYY-MM           (optional)
    """
    email = request.args.get('email')
    month = request.args.get('month')  # e.g. '2025-07'
    if not email:
        return jsonify({'error': 'Missing email parameter'}), 400

    q = TimerRecord.query.filter_by(email=email)
    if month:
        try:
            year, mon = month.split('-')
            year, mon = int(year), int(mon)
            q = q.filter(
                db.extract('year', TimerRecord.date) == year,
                db.extract('month', TimerRecord.date) == mon
            )
        except:
            return jsonify({'error': 'Invalid month format'}), 400

    records = q.order_by(TimerRecord.date.desc(), TimerRecord.created_at.desc()).all()
    return jsonify([_record_to_dict(r) for r in records]), 200

@timer_bp.route('/timer_records/<int:rec_id>', methods=['PUT'])
def update_timer_record(rec_id):
    """
    Body JSON:
      {
        "date": "YYYY-MM-DD",
        "minutes": <int>,
        "mode": "stopwatch"|"countdown"|"pomodoro"
      }
    """
    data = request.get_json() or {}
    rec = TimerRecord.query.get(rec_id)
    if not rec:
        return jsonify({'error': 'Record not found'}), 404

    date_str = data.get('date')
    minutes  = data.get('minutes')
    mode     = data.get('mode')
    if not all([date_str, minutes is not None, mode]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        rec.date    = datetime.strptime(date_str, '%Y-%m-%d').date()
        rec.minutes = int(minutes)
        rec.mode    = mode
        db.session.commit()
        return jsonify(_record_to_dict(rec)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@timer_bp.route('/timer_records/<int:rec_id>', methods=['DELETE'])
def delete_timer_record(rec_id):
    rec = TimerRecord.query.get(rec_id)
    if not rec:
        return jsonify({'error': 'Record not found'}), 404
    try:
        db.session.delete(rec)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
