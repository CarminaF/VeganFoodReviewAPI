from init import db, ma 
from marshmallow import fields

class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    description = db.Column(db.String)

    restaurants = db.relationship('Restaurant', back_populates='type')

class TypeSchema(ma.Schema):
    restaurant = fields.Nested('RestaurantSchema', exclude=['type'])

    class Meta:
        fields = ('id', 'type', 'description', 'restaurants')

type_schema = TypeSchema()
types_schema = TypeSchema(many=True)