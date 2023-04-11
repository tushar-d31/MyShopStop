from http import server
from flask import redirect,render_template,url_for,flash,request,session,current_app
from shop import db,app,photos,search
from .models import Brand,Category,Product
from .forms import Addproducts
from shop.seller.models import product_seller,Seller
import secrets
import os

def brands():
    brands=Brand.query.join(Product,(Brand.id==Product.brand_id)).all()
    return brands

def categories():
    categories=Category.query.join(Product,(Category.id==Product.category_id)).all()
    return categories

@app.route('/')
def home():
    page=request.args.get('page',1,type=int)
    products=Product.query.filter(Product.stock>0).order_by(Product.id.desc()).paginate(page=page,per_page=8)
    return render_template('products/index.html',products=products,brands=brands(),categories=categories())

@app.route('/searchresult')
def searchresult():
    searchword=request.args.get('q')
    products=Product.query.msearch(searchword,fields=['name','desc'], limit=6)
    return render_template('products/searchresult.html',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product=Product.query.get_or_404(id)
    seller_details=db.session.query(Seller.email,Seller.address).join(product_seller).filter_by(seller_id=Seller.id ,product_id=Product.id).first()
    print(seller_details)
    return render_template('products/single_page.html',product=product,brands=brands(),categories=categories(),seller_details=seller_details)

@app.route('/brand/<int:id>')
def getbrand(id):
    page=request.args.get('page',1,type=int)
    get_brand=Brand.query.filter_by(id=id).first_or_404()
    brand=Product.query.filter_by(brand=get_brand).paginate(page=page,per_page=8)
    return render_template('products/index.html',brand=brand,brands=brands(),categories=categories(),get_brand=get_brand)

@app.route('/categories/<int:id>')
def getcategory(id):
    page=request.args.get('page',1,type=int)
    get_cat=Category.query.filter_by(id=id).first_or_404()
    get_cat_prod=Product.query.filter_by(category=get_cat).paginate(page=page,per_page=8)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,categories=categories(),
    brands=brands(),get_cat=get_cat)

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please Log in first','danger')
        return redirect(url_for('login'))
    if request.method=='POST':
        getbrand= request.form.get('brand')
        brand=Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {getbrand} was added','success')
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please Login First!','danger')
    updatebrand=Brand.query.get_or_404(id)
    brand=request.form.get('brand')
    if request.method=='POST':
        updatebrand.name=brand   
        flash('The brand was updated!','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>',methods=['POST'])
def deletebrand(id):
    brand=Brand.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted!','success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} can\'t be deleted','warning')
    return redirect(url_for('admin'))


@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please Log in first','danger')
        return redirect(url_for('login'))
    if request.method=='POST':
        getcat= request.form.get('category')
        category=Category(name=getcat)
        db.session.add(category)
        flash(f'The Category {getcat} was added','success')
        db.session.commit()
        
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please Login First!','danger')
    updatecat=Category.query.get_or_404(id)
    category=request.form.get('category')
    if request.method=='POST':
        updatecat.name=category   
        flash('The category was updated!','success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html',updatecat=updatecat)

@app.route('/deletecategory/<int:id>',methods=['POST'])
def deletecategory(id):
    category=Category.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted!','success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} can\'t be deleted','warning')
    return redirect(url_for('admin'))


@app.route('/addprod', methods=['GET', 'POST'])
def addprod():
    if 'email' not in session:
        flash(f'Please Log in first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
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
        flash(f'The product {name} has be added','success')
        db.session.commit()    
        return redirect(url_for('admin'))
    return render_template('products/addprod.html', form=form, brands=brands, categories=categories, seller=Seller)

@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Product.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.desc.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash('The product was updated','success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.desc.data = product.desc
    return render_template('products/updateproduct.html',form=form
    ,brands=brands,categories=categories,product=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product=Product.query.get_or_404(id)
    if request.method=='POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
              
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted!','success')
        return redirect(url_for('admin'))
    flash(f'Sorry! Can\'t delete the product!','danger') 
    return redirect(url_for('admin'))
