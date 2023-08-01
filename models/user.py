from init import db, ma
from marshmallow import fields
'''
Create User class as a model using extension of db.Model
'''
class User(db.Model):
    __tablename__ = 'users'

    # Define data types
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    # When getting user details, the below allows one to see the reviews made by a user
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')


'''
Create UserSchema class as a schema
'''
class UserSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=['user'])
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'is_admin', 'reviews')


'''
Initialize schemas for retrieving one or multiple user entries
'''
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])