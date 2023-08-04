from flask import Blueprint, request 
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

# Create blueprint with prefix "/auth"
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Create admin_required decorator for certain delete and put/patch routes
def admin_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, ** kwargs)
        else:
            return {'error': 'Only admins are authorized to do this action'}
    return wrapper


# Create new account with email, username and password
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:        
        body_data = request.get_json()

        user = User()
        user.username = body_data.get('username')
        user.email = body_data.get('email')
        # store encrypted password in psql database
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            
            # Differentiate between which of two values (email or username) need to be unique
            constraint_name = err.orig.diag.constraint_name

            if 'email' in str(constraint_name):
                return {'error': 'Email address already in use'}, 409
            if 'username' in str(constraint_name):
                return {'error': 'Username already taken'}, 409
        # Error to ensure non-nullable fields are populated by the user
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} field is required'}, 409


# Users can log in using either with the email or username and password
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    email_or_username = body_data.get('email_or_username')

    # Select entry from user table where the 'email or username' field matches the 'email' or 'username' field
    stmt = db.select(User).where(db.or_(User.email == email_or_username, User.username == email_or_username))
    user = db.session.scalar(stmt)

    # ensure user login is correct and password correctly matches with database
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {
                'username': user.username, 
                'email': user.email, 
                'token': token, 
                'is_admin': user.is_admin,
                'message': 'Login successful'}
    else:
        return {'error': 'Incorrect login details'}, 401
    
