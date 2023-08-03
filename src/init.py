from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

'''
Instances of the libraries/toolkit/packages are being initialized below so that
you can just import them to main using its variable names

- SQL Alchemy: Python SQL toolkit and Object Relational Mapper
- Marshmallow: Object Relational Mapping library to convert objects (such as database schemas) to and from Python data types
- Bcrypt: Library for generating strong hashing values
- JWTManager: For JSON Web Token (JWT) Authentication
'''
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()