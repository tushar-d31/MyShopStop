from shop import db,login_manager
from flask_login import UserMixin
from datetime import datetime
import json

@login_manager.user_loader
def user_loader(customer_id):
    return Customer.query.get(customer_id)


class Customer(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=False)
    username=db.Column(db.String(50),unique=False)
    email=db.Column(db.String(80),unique=False)
    password=db.Column(db.String(160),unique=False)
    phoneno=db.Column(db.String(50),unique=False)
    country=db.Column(db.String(50),unique=False)
    state=db.Column(db.String(50),unique=False)
    city=db.Column(db.String(50),unique=False)
    address=db.Column(db.String(50),unique=False)


    def __repr__(self):
        return '<Customer %c' %self.name


class JsonEncodedDict(db.TypeDecorator):
    impl=db.Text

    def process_bind_param(self,value,dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self,value,dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    invoice=db.Column(db.String(20),unique=True,nullable=False)
    status=db.Column(db.String(20),default='Pending',nullable=False)
    customer_id=db.Column(db.Integer,unique=False,nullable=False)
    order_date=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    orders=db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<CustomerOrder %o' %self.invoice

db.create_all()

