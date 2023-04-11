from shop import db


class Brand(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False,unique=True)

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False,unique=True)

class Product(db.Model):
    __tablename__='product'
    __searchable__=['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.Numeric(10,2),nullable=False)
    discount=db.Column(db.Integer,default=0)
    stock=db.Column(db.Integer,nullable=False)
    colors=db.Column(db.Text,nullable=False)
    desc = db.Column(db.Text, nullable=False)
    
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    image_1=db.Column(db.String(150),nullable=False)
    image_2=db.Column(db.String(150),nullable=False)
    image_3=db.Column(db.String(150),nullable=False)
   

    def __repr__(self):
        return '<Product %r>' % self.name


db.create_all()

