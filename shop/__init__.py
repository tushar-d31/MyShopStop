from functools import wraps
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads
from flask_msearch import Search
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
import os
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshopstop.db'
app.config['SECRET_KEY']='mysecretkey'

basedir=os.path.abspath(os.path.dirname(__file__))
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir,"static/images")
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
search=Search()
search.init_app(app)

migrate=Migrate(app,db)
with app.app_context():
    if db.engine.url.drivername=="sqlite":
        migrate.init_app(app,db,render_as_batch=True)
    else:
        migrate.init_app(app,db)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='seller_login'

login_manager.needs_refresh_message_category='danger'
login_manager.login_message=u"Please Login first!"
login_manager.login_message_category="danger"


from shop.admin import routes
from shop.carts import carts
from shop.products import routes
from shop.customers import routes
from shop.seller import routes


