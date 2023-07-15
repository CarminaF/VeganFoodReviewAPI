from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.category import Category
from models.restaurant import Restaurant

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

    categories = [
        Category (
            category='Vegan',
            description='Fully vegan restaurant'
        ),
        Category (
            category='Vegetarian',
            description='Fully vegetarian restaurant with vegan options'
        ),
        Category (
            category='Omnivore',
            description='An omni/normal restaurant with vegan options'
        )
    ]
    db.session.add_all(categories)

    restaurants = [
        Restaurant (
            name='Hungry Jacks',
            location='Nationwide',
            contact_number='Varies by location',
            website='https://www.hungryjacks.com.au/home',
            category=categories[2]
        ),
        Restaurant (
            name='Staazi & Co',
            location='224 Grenfell St, Adelaide, South Australia',
            contact_number='+61-416202544',
            website='https://www.staaziandco.com.au/',
            category=categories[0]
        ),
        Restaurant (
            name='Comeco Foods',
            location='524 King Street, Newtown, NSW 2042',
            contact_number='534264357',
            website='https://www.comecofoods.com.au/',
            category=categories[0]
        ),
        Restaurant (
            name='Son in Law',
            location='211 Latrobe St, Melbourne, Victoria, Australia, 3000',
            contact_number='546213654',
            website='http://www.soninlaw.com.au/',
            category=categories[2]
        ),
        Restaurant (
            name='Two-Bit Villains',
            location='Shop 150, Lvl One, Adelaide Arcade, SA, 5000',
            contact_number='424383224',
            website='https://www.twobitvillains.com.au/',
            category=categories[1]
        )
    ]
    db.session.add_all(restaurants)

    db.session.commit()

    print('Tables seeded')



