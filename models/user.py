from init import db, ma
'''
Create User class as a model using extension of db.Model
'''
class User(db.Model):
    __tablename__ = 'users'

    # Define data types
    id = db.Column(db.Integer, primary=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)


'''
Create UserSchema class as a 
'''
class UserSchema(ma.Schema):
    fields = ('id', 'username', 'password', 'email', 'is_admin')

'''
Initialize schemas for retrieving one or multiple user entries
'''
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])