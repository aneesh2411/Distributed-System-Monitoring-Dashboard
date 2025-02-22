"""Authentication API endpoints."""
from datetime import timedelta
from flask_restx import Namespace, Resource, fields
from flask import request
from database import get_db
from auth.models import User
from auth.jwt import create_access_token
from auth.decorators import admin_required

# Create namespace
ns = Namespace('auth', description='Authentication operations')

# Models
login_model = ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

user_create_model = ns.model('UserCreate', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(default=False, description='Admin status')
})

token_model = ns.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'token_type': fields.String(description='Token type')
})

@ns.route('/login')
class Login(Resource):
    """Login endpoint."""

    @ns.expect(login_model)
    @ns.marshal_with(token_model)
    def post(self):
        """Login and get access token."""
        data = request.json
        
        with get_db() as db:
            user = db.query(User).filter(User.username == data['username']).first()
            if not user or not user.verify_password(data['password']):
                ns.abort(401, message='Invalid credentials')
            
            access_token = create_access_token(
                data={'sub': user.username},
                expires_delta=timedelta(minutes=30)
            )
            
            return {
                'access_token': access_token,
                'token_type': 'bearer'
            }

@ns.route('/users')
class Users(Resource):
    """User management endpoints."""

    @admin_required
    @ns.expect(user_create_model)
    def post(self):
        """Create a new user (admin only)."""
        data = request.json
        
        with get_db() as db:
            if db.query(User).filter(User.username == data['username']).first():
                ns.abort(400, message='Username already exists')
            
            if db.query(User).filter(User.email == data['email']).first():
                ns.abort(400, message='Email already exists')
            
            user = User(
                username=data['username'],
                email=data['email'],
                is_admin=data.get('is_admin', False)
            )
            user.set_password(data['password'])
            
            db.add(user)
            db.commit()
            
            return user.to_dict(), 201 