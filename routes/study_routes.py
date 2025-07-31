# routes/study_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Todo, Note

study_bp = Blueprint('study', __name__)

#
# --- Todo endpoints ---
#

@study_bp.route('/todos', methods=['GET'])
def get_todos():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    todos = Todo.query.filter_by(user_email=email).order_by(Todo.created_at.desc()).all()
    return jsonify([
        {'id': t.id, 'name': t.name, 'completed': t.completed}
        for t in todos
    ]), 200


@study_bp.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json() or {}
    email = data.get('email')
    name = data.get('name')
    if not email or not name:
        return jsonify({'error': 'Missing fields'}), 400

    todo = Todo(user_email=email, name=name)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo added', 'id': todo.id}), 200


@study_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json() or {}
    todo = Todo.query.get_or_404(todo_id)
    if 'name' in data:
        todo.name = data['name']
    if 'completed' in data:
        todo.completed = bool(data['completed'])
    db.session.commit()
    return jsonify({'message': 'Todo updated'}), 200


@study_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200


#
# --- Note endpoints ---
#

@study_bp.route('/notes', methods=['GET'])
def get_notes():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    notes = Note.query.filter_by(user_email=email).order_by(Note.created_at.desc()).all()
    return jsonify([
        {
            'id': n.id,
            'title': n.title,
            'subject': n.subject,
            'content': n.content
        }
        for n in notes
    ]), 200


@study_bp.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json() or {}
    email = data.get('email')
    title = data.get('title')
    subject = data.get('subject')
    content = data.get('content')
    if not all([email, title, subject, content]):
        return jsonify({'error': 'Missing fields'}), 400

    note = Note(
        user_email=email,
        title=title,
        subject=subject,
        content=content
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added', 'id': note.id}), 200


@study_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json() or {}
    note = Note.query.get_or_404(note_id)
    if 'title' in data:
        note.title = data['title']
    if 'subject' in data:
        note.subject = data['subject']
    if 'content' in data:
        note.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Note updated'}), 200


@study_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'}), 200
