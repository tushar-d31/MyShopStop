from shop import db
from flask_login import UserMixin


product_seller=db.Table('product_seller',
                        db.Column('product_id',db.Integer,db.ForeignKey('product.id'),primary_key=True),
                        db.Column('seller_id',db.Integer,db.ForeignKey('seller.id'),primary_key=True))         


class Seller(db.Model,UserMixin):
    __tablename__='seller'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=False)
    email=db.Column(db.String(80),unique=False)
    password=db.Column(db.String(160),unique=False)
    phoneno=db.Column(db.String(50),unique=False)

    product = db.relationship('Product', secondary=product_seller, lazy='subquery',
        backref=db.backref('products', lazy=True))

    address=db.Column(db.Text(100),unique=False)
    gst_no=db.Column(db.String(20),unique=True)
    pan_no=db.Column(db.String(20),unique=True)

    def __repr__(self):
        return '<Seller %s' %self.name

db.create_all()

