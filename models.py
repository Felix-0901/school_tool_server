from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(50), nullable=False)  # 年月日時分
    location = db.Column(db.String(255))
    note = db.Column(db.Text)

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # 格式 YYYY-MM-DD
    content = db.Column(db.Text)

    def __repr__(self):
        return f"<Diary {self.user_email} {self.date} {self.title}>"

