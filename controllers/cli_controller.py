from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')


@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print('Tables dropped')


@db_commands.cli.command('seed')
def seed_db():
    users = [
        User (
            username='admin',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            email='admin@vegfoodreview.com',
            is_admin=True
        ),
        User (
            username='veganfoodlover',
            password=bcrypt.generate_password_hash('idonteatmeat'),
            email='veganfoodlover@foodie.com'
        ),
        User (
            username='veggiecurious',
            password=bcrypt.generate_password_hash('istilleatmeat'),
            email='curiousclaire@veggiecurious.com'
        ),
        User (
            username='daretobedairyfree',
            password=bcrypt.generate_password_hash('dairyisscary'),
            email='dazzaisdairyfree@yahoo.com'
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    print('Tables seeded')



