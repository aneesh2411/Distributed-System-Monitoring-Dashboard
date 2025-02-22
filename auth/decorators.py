"""Authentication decorators."""
from functools import wraps
from flask import request, g
from flask_restx import abort
from database import get_db
from .models import User
from .jwt import decode_token

def login_required(f):
    """Decorator to require authentication for an endpoint."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401, message='Missing authorization header')
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1]
            payload = decode_token(token)
            
            with get_db() as db:
                user = db.query(User).filter(User.username == payload['sub']).first()
                if not user:
                    abort(401, message='Invalid user')
                g.current_user = user
                
        except (IndexError, ValueError):
            abort(401, message='Invalid token')
            
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to require admin privileges for an endpoint."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not g.current_user.is_admin:
            abort(403, message='Admin privileges required')
        return f(*args, **kwargs)
    return decorated

def api_key_required(f):
    """Decorator to allow API key authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            abort(401, message='Missing API key')
        
        with get_db() as db:
            user = db.query(User).filter(User.api_key == api_key).first()
            if not user:
                abort(401, message='Invalid API key')
            g.current_user = user
            
        return f(*args, **kwargs)
    return decorated 