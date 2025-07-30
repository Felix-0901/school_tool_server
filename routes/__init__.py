from .auth import register_auth_routes
from .task import register_task_routes

def register_routes(app):
    register_auth_routes(app)
 

def register_routes(app):
    register_auth_routes(app)
    register_task_routes(app)
