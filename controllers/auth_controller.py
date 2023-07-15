from flask import Blueprint, request 
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:        
        body_data = request.get_json()

        user = User()
        user.username = body_data.get('username')
        user.email = body_data.get('email')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            
            constraint_name = err.orig.diag.constraint_name

            if 'email' in str(constraint_name):
                return {'error': 'Email address already in use'}, 409
            if 'username' in str(constraint_name):
                return {'error': 'Username already taken'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} field is required'}, 409
