from init import db, ma 
from marshmallow import fields

# Establish food table and columns
class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False) #?

    # Define relationships with restaurants and reviews
    restaurant = db.relationship('Restaurant', back_populates='foods')
    reviews = db.relationship('Review', back_populates='food', cascade='all, delete')
   
# Initialise Food schema. Nest restaurants and reviews
class FoodSchema(ma.Schema):
    restaurant = fields.Nested('RestaurantSchema', only=['id', 'name', 'type'])
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['food']))

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'restaurant', 'reviews')
        ordered = True

# Initialize schemas for retrieving one or multiple user entries
food_schema = FoodSchema()
foods_schema = FoodSchema(many=True)