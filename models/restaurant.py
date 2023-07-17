from init import db, ma 
from marshmallow import fields

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    contact_number = db.Column(db.String)
    website = db.Column(db.String)

    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)

    type = db.relationship('Type', back_populates='restaurants')

class RestaurantSchema(ma.Schema):
    type = fields.Nested('TypeSchema', only=['id', 'type'])
    
    class Meta:
        fields = ('id', 'name', 'location', 'contact_number', 'website', 'type')
        ordered = True

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)