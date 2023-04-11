from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms import Form,IntegerField,StringField,BooleanField,TextAreaField,validators,DecimalField
from werkzeug.utils import secure_filename

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    desc = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])

    sellername = StringField('Seller Name',[validators.DataRequired()] ,render_kw={'readonly': True})
    selleremail = StringField('Seller email',[validators.DataRequired()] ,render_kw={'readonly': True})
    selleraddress = StringField('Seller address',[validators.DataRequired()] ,render_kw={'readonly': True})

    image_1 = FileField('Image-1', validators=[ FileAllowed(
        ['jpg', 'png', 'jpeg'],'Images only!')])
    image_2 = FileField('Image-2', validators=[ FileAllowed(
        ['jpg', 'png', 'jpeg'],'Images only!')])
    image_3 = FileField('Image-3', validators=[ FileAllowed(
        ['jpg', 'png', 'jpeg'],'Images only!')])
