# models.py

from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

class User(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    first_name     = db.Column(db.String(100), nullable=False)
    last_name      = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    password_hash  = db.Column(db.String(512), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    task_name  = db.Column(db.String(255), nullable=False)
    time       = db.Column(db.String(50), nullable=False)  # 年月日時分
    location   = db.Column(db.String(255))
    note       = db.Column(db.Text)


class Diary(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    title      = db.Column(db.String(255), nullable=False)
    date       = db.Column(db.String(10), nullable=False)  # 格式 YYYY-MM-DD
    content    = db.Column(db.Text)

    def __repr__(self):
        return f"<Diary {self.user_email} {self.date} {self.title}>"


class TimerRecord(db.Model):
    __tablename__ = 'timer_records'
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    date       = db.Column(db.Date, nullable=False)
    minutes    = db.Column(db.Integer, nullable=False)
    mode       = db.Column(db.String(20), nullable=False)  # stopwatch|countdown|pomodoro
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---- 新增：Todo 待辦事項 ----

class Todo(db.Model):
    __tablename__ = 'todos'
    id           = db.Column(db.Integer, primary_key=True)
    user_email   = db.Column(db.String(120), nullable=False)
    name         = db.Column(db.String(255), nullable=False)
    completed    = db.Column(db.Boolean, default=False, nullable=False)
    created_at   = db.Column(db.Date, default=date.today, nullable=False)

    def __repr__(self):
        return f"<Todo {self.user_email} {self.name} completed={self.completed}>"


# ---- 新增：Note 筆記記錄 ----

class Note(db.Model):
    __tablename__ = 'notes'
    id           = db.Column(db.Integer, primary_key=True)
    user_email   = db.Column(db.String(120), nullable=False)
    title        = db.Column(db.String(255), nullable=False)
    subject      = db.Column(db.String(100), nullable=False)
    content      = db.Column(db.Text, nullable=False)
    created_at   = db.Column(db.Date, default=date.today, nullable=False)

    def __repr__(self):
        return f"<Note {self.user_email} {self.title} ({self.subject})>"

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(255), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }