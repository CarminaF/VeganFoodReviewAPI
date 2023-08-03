from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.restaurant import Restaurant
from models.food import Food
from models.review import Review
from datetime import date


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
            password=bcrypt.generate_password_hash('idonteatmeat').decode('utf-8'),
            email='veganfoodlover@foodie.com'
        ),
        User (
            username='veggiecurious',
            password=bcrypt.generate_password_hash('istilleatmeat').decode('utf-8'),
            email='curiousclaire@veggiecurious.com'
        ),
        User (
            username='daretobedairyfree',
            password=bcrypt.generate_password_hash('dairyisscary').decode('utf-8'),
            email='dazzaisdairyfree@yahoo.com'
        )
    ]
    db.session.add_all(users)

    restaurants = [
        Restaurant (
            name='Hungry Jacks',
            location='Nationwide',
            contact_number='Varies by location',
            website='https://www.hungryjacks.com.au/home',
            type='Vegan options available'
        ),
        Restaurant (
            name='Staazi & Co',
            location='224 Grenfell St, Adelaide, South Australia',
            contact_number='+61-416202544',
            website='https://www.staaziandco.com.au/',
            type='Vegan'
        ),
        Restaurant (
            name='Comeco Foods',
            location='524 King Street, Newtown, NSW 2042',
            contact_number='534264357',
            website='https://www.comecofoods.com.au/',
            type='Vegan'
        ),
        Restaurant (
            name='Son in Law',
            location='211 Latrobe St, Melbourne, Victoria, Australia, 3000',
            contact_number='546213654',
            website='http://www.soninlaw.com.au/',
            type='Vegan options available'
        ),
        Restaurant (
            name='Two-Bit Villains',
            location='Shop 150, Lvl One, Adelaide Arcade, SA, 5000',
            contact_number='424383224',
            website='https://www.twobitvillains.com.au/',
            type='Vegetarian'
        )
    ]
    db.session.add_all(restaurants)

    foods = [
        Food (
            name='Vegan Whopper Cheeseburger',
            description='Vegan burger. Vegan patty is made from mashed vegetables. Has vegan mayo and cheese',
            price=6.75,
            restaurant=restaurants[0],
        ),
        Food (
            name='Plant Based Whopper Burger',
            description='Vegan burger with meat-like plant based patty. Need to specify vegan cheese and vegan mayo',
            price=8.95,
            restaurant=restaurants[0]
        ),
        Food (
            name='Vegan Duck Character Bao',
            description='Vegan mock duck with cucumber, hoisin sauce and coriander inside a character bao bun',
            price=8.50,
            restaurant=restaurants[3]
        ),
        Food (
            name='Lamb Yiros',
            description='Vegan greek food. Vegan lamb made from soy meat',
            price=16,
            restaurant=restaurants[1]
        ),
        Food (
            name='Vegan Lamb AB/HSP',
            description='AB “lamb” layered over hot chips then topped with home made tzatziki & another sauce of your choice (tomato, bbq or sriracha).',
            price=18,
            restaurant=restaurants[1],
        ),
        Food (
            name='Vegan Japanese curry',
            description='Homemade vegan Japanese curry with rice and tofu cutlet',
            price=22,
            restaurant=restaurants[2]
        ),
        Food (
            name='Vegan Almond Croissant',
            description='Vegan croissant with almonds',
            price=5.5,
            restaurant=restaurants[4]
        ),
    ]
    db.session.add_all(foods)

    reviews = [
        Review (
            rating=3,
            review_title='Could be better',
            review_text='Veggie patty is kind of bland',
            timestamp=date.today(),
            food=foods[0],
            user=users[1]
        ),
        Review (
            rating=2,
            review_title='Not the best',
            review_text='Patty is like mashed potato',
            timestamp=date.today(),
            food=foods[0],
            user=users[2]
        ),
        Review (
            rating=5,
            review_title='Best vegan yiros ever',
            review_text='Soy lamb tastes just like meat',
            timestamp=date.today(),
            food=foods[3],
            user=users[2]
        ),
        Review (
            rating=5,
            review_title='Did not disappoint',
            review_text='The mock lamb was amazing and juicy. Quick service too!',
            timestamp=date.today(),
            food=foods[3],
            user=users[3]
        ),
    ]
    db.session.add_all(reviews)
    db.session.commit()

    print('Tables seeded')



