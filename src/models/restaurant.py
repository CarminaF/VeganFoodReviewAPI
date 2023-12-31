from init import db, ma 
from marshmallow import fields, ValidationError, validates

VALID_TYPES = ('Vegan', 'Vegetarian', 'Vegan options available')

# Initialise Restaurant tables and column
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    contact_number = db.Column(db.String)
    website = db.Column(db.String)
    
    
    # The 'type' determines whether an establishment
    # is fully vegan, fully vegetarian or 
    # an omni restaurant with vegan options
    
    type = db.Column(db.String, nullable=False)

    # Delete all food associated to a restaurant if restaurant is deleted    
    foods = db.relationship('Food', back_populates='restaurant', cascade='all, delete') 

# Initialise Restaurant schema, nest list of foods
class RestaurantSchema(ma.Schema):
    foods = fields.List(fields.Nested('FoodSchema', exclude=['restaurant', 'reviews']))
    
    @validates('type')
    def validate_type(self, value):
        if value.lower not in (t.lower() for t in VALID_TYPES):
            raise ValidationError(f'Invalid restaurant type')
    class Meta:
        fields = ('id', 'name', 'location', 'contact_number', 'website', 'type', 'foods')
        ordered = True

# Initialize schemas for retrieving one or multiple user entries
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)