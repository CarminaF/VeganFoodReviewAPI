from init import db, ma 
from marshmallow import fields

VALID_TYPES = ('Vegan', 'Vegetarian', 'Vegan options available')


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    contact_number = db.Column(db.String)
    website = db.Column(db.String)
    
    '''
    The 'type' determines whether an establishment
    is fully vegan, fully vegetarian or 
    an omni restaurant with vegan options
    '''
    type = db.Column(db.String, nullable=False)

    '''
    Delete all food associated to a restaurant if restaurant is deleted
    '''
    foods = db.relationship('Food', back_populates='restaurant', cascade='all, delete') 

    
class RestaurantSchema(ma.Schema):
    foods = fields.List(fields.Nested('FoodSchema', exclude=['restaurant', 'reviews']))
    
    class Meta:
        fields = ('id', 'name', 'location', 'contact_number', 'website', 'type', 'foods')
        ordered = True


restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)