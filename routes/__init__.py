# routes/__init__.py

from .auth import register_auth_routes
from .task import register_task_routes
from .diary import register_diary_routes
from .timer_record import timer_bp
from .study_routes import study_bp
from .user_routes import user_bp
from .announcement_routes import announcement_bp

def register_routes(app):
    # 原本的各個 Blueprint
    register_auth_routes(app)
    register_task_routes(app)
    register_diary_routes(app)
    # 註冊計時器記錄
    app.register_blueprint(timer_bp)
    # 註冊 Study 頁面的 Todo & Note Blueprint
    app.register_blueprint(study_bp)
    # 註冊 User 頁面的 Blueprint
    app.register_blueprint(user_bp)
    app.register_blueprint(announcement_bp)