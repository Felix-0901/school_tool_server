from .task import register_task_routes
from .auth import register_auth_routes
from .diary import register_diary_routes   # 新增這行

def register_routes(app):
    register_auth_routes(app)
    register_task_routes(app)
    register_diary_routes(app)              # 新增這行
