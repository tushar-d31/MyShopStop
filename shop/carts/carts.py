from flask import redirect,render_template,url_for,flash,request,session,current_app
from shop import db,app
from shop.products.models import Product
from shop.products.routes import brands,categories


def MergeDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1+dict2 
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False


@app.route('/addtocart',methods=['POST'])
def AddtoCart():
    try:
        product_id=request.form.get('product_id')
        quantity=request.form.get('quantity')
        colors=request.form.get('colors')
        product=Product.query.filter_by(id=product_id).first()

        if product_id and quantity and colors and request.method=='POST':
            DictItems={product_id:{'name':product.name, 'price':product.price , 'discount':product.discount,
            'color':colors,'quantity':quantity, 'image':product.image_1,'colors':product.colors}}

            if 'Cart' in session:
                print(session['Cart'])
                if product_id  in session['Cart']:
                    for key, item in session['Cart'].items():
                        if int(key) == int(product_id):
                            session.modified=True
                            item['quantity'] += 1
                                
                else:
                    session['Cart']=MergeDicts(session['Cart'],DictItems)
                    return redirect(request.referrer)
            else:
                session['Cart']=DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getcart():
    if 'Cart' not in session:
        return redirect(request.referrer)      
    subtotal=0
    total=0
    for key,product in session['Cart'].items():
        discount=(product['discount']/100)*float(product['price'])
        subtotal+=float(product['price']) * int(product['quantity'])
        subtotal-=discount
        total=float("%0.2f" % (1*subtotal))
    return render_template('products/carts.html', total=total,brands=brands(),categories=categories()) 

@app.route('/updatecart/<int:id>',methods=['POST'])
def updatecart(id):
    if 'Cart' not in session and len(session['Cart'])<=0 :
         return redirect(url_for('home')) 
    if request.method=='POST':
        quantity= request.form.get('quantity')
        color=request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Cart'].items():
                if int(key) == id:
                    item['quantity']=quantity
                    item['color']=color
                    flash(f'Your Cart was updated!','success')
                    return redirect(url_for('getcart'))
        except Exception as e:
            print(e)
            return (redirect(url_for('getcart')))

@app.route('/deleteprod/<int:id>')
def deleteprod(id):
    if 'Cart' not in session and len(session['Cart'])<=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Cart'].items():
            if int(key) == id:
                session['Cart'].pop(key,None)
                flash(f'Your Cart was updated!','success')
                return redirect(url_for('getcart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))

@app.route('/emptycart')
def emptycart():
    try:
        session.pop('Cart',None)    
        return redirect(url_for('home'))
    except Exception as e:
        print(e)