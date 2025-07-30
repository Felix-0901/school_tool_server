from flask import request, jsonify
from models import Task
from database import db

def register_task_routes(app):
    @app.route('/add_task', methods=['POST'])
    def add_task():
        data = request.get_json()
        email = data.get('email')
        task_name = data.get('task_name')
        time = data.get('time')
        location = data.get('location')
        note = data.get('note')

        if not all([email, task_name, time]):
            return jsonify({'message': 'Missing required fields'}), 400

        new_task = Task(
            user_email=email,
            task_name=task_name,
            time=time,
            location=location,
            note=note
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task added successfully'}), 200

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        email = request.args.get('email')
        if not email:
            return jsonify({'message': 'Email is required'}), 400

        tasks = Task.query.filter_by(user_email=email).all()
        result = []
        for task in tasks:
            result.append({
                'id': task.id,
                'task_name': task.task_name,
                'time': task.time,
                'location': task.location,
                'note': task.note
            })

        return jsonify({'tasks': result}), 200
