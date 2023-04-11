from itertools import product
from math import prod
from flask import render_template, session,request, redirect, url_for,flash
from shop import app, db,bcrypt,photos,login_manager
from flask_login import current_user, login_required, login_user, logout_user
from .forms import SellerRegistration,SellerLogin
from .models import Seller,product_seller
from shop.products.models import Product,Brand,Category
from shop.products.forms import Addproducts 
import os,secrets

@app.route('/seller/home')
@login_required
def seller_home():
    if not current_user.is_authenticated:
        return redirect(url_for('seller_login'))
    seller_id=current_user.id
    products=db.session.query(Product.id,Product.name,Product.price, Product.discount,Product.image_1,Product.stock).join(product_seller).filter_by(seller_id=seller_id).all()
    return render_template('seller/home.html',title='Seller Page',products=products)

@app.route('/seller/register', methods=['GET', 'POST'])
def seller_register():
    form = SellerRegistration(request.form)
    if request.method == 'POST' and form.validate():
        hash_password=bcrypt.generate_password_hash(form.password.data)
        seller = Seller(name=form.name.data,email= form.email.data,
                    password=hash_password,phoneno=form.phoneno.data,
                    address=form.address.data,gst_no=form.gst_no.data,pan_no=form.pan_no.data)
        db.session.add(seller)
        flash(f'Welcome {form.name.data}, Thanks for becoming a seller at MyShopStop','success')
        db.session.commit()
        return redirect(url_for('seller_login'))
    return render_template('seller/register.html', form=form)

@app.route('/seller/login',methods=['GET','POST'])
def seller_login():
    form=SellerLogin(request.form)
    if request.method == 'POST' and form.validate():
        seller = Seller.query.filter_by(email=form.email.data).first()
        if seller and bcrypt.check_password_hash(seller.password,form.password.data):
            login_user(seller)
            flash(f'Welcome {form.email.data},You are logged in.','success')
            return redirect(request.args.get('next') or url_for('seller_home'))
        else:
            flash('Wrong password! Try Again','danger')
    return render_template('seller/login.html',form=form)

@app.route('/seller/addprod', methods=['GET', 'POST'])
@login_required
def seller_add_product():
    if current_user.is_authenticated:
        seller_id=current_user.id
        form = Addproducts(request.form)
        seller=Seller.query.filter_by(id=seller_id).first()
        brands = Brand.query.all()
        categories = Category.query.all()
        if request.method == 'POST':
            name=form.name.data
            price=form.price.data
            discount=form.discount.data
            stock=form.stock.data
            colors=form.colors.data
            desc=form.desc.data
            brand=request.form.get('brand')
            category=request.form.get('category')
            image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            product=Product(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,
            brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
            db.session.add(product)
            db.session.commit()
            flash(f'The product {name} has be added','success')
            seller.product.append(product)
            db.session.commit()    
            return redirect(url_for('seller_home'))
        return render_template('products/addprod.html', form=form, brands=brands, categories=categories,seller=seller)

@app.route('/seller/logout',methods=['GET','POST'])
def seller_logout():
    logout_user()
    return redirect(url_for('seller_login'))