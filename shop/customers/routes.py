from flask import redirect,render_template,url_for,flash,request,session,current_app,make_response
from flask_login import login_required,current_user,logout_user,login_user
from shop import db,app,photos,search,bcrypt,login_manager
from .forms import CustomerRegistration,CustomerLogin
from .models import Customer,CustomerOrder
import secrets
import os
import pdfkit


@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
    form=CustomerRegistration()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register_user=Customer(name=form.name.data,username=form.username.data,email=form.email.data,
        password=hash_password,country=form.country.data,state=form.state.data,city=form.city.data,
        address=form.address.data,phoneno=form.phoneno.data)
        db.session.add(register_user)
        flash(f'Thank You {form.name.data} for registering with us!','success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
       
    return render_template('customers/register.html',form=form)

@app.route('/customer/login',methods=['GET','POST'])
def customerLogin():
    form=CustomerLogin()
    if form.validate_on_submit() :
        user=Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'You are now logged in!','success')
            next=request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Incorrect email and password!','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customers/login.html',form=form)

@app.route('/customer/logout')
def customerLogout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id=current_user.id
        invoice = secrets.token_hex(5)
        try:
            order=CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Cart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Cart')
            flash(f'Your order is confirmed!.Thank you for shopping with us :)','success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash(f'Something went wrong!','danger')
            return redirect(url_for('getcart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        total=0
        subTotal=0
        customer_id=current_user.id 
        customer=Customer.query.filter_by(id=customer_id).first()
        orders=CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount=(product['discount']/100)*float(product['price'])
            subTotal+=float(product['price'])*int(product['quantity'])
            subTotal-=discount
            total=float("%.2f" %(subTotal))
    
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customers/order.html',customer=customer,orders=orders,invoice=invoice,
    subTotal=subTotal,total=total) 

@app.route('/generate_pdf/<invoice>',methods=['POST'])
@login_required
def generate_pdf(invoice):
    if current_user.is_authenticated:
        total=0
        subTotal=0
        customer_id=current_user.id 
        if request.method=='POST':
            customer=Customer.query.filter_by(id=customer_id).first()
            orders=CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount=(product['discount']/100)*float(product['price'])
                subTotal+=float(product['price'])*int(product['quantity'])
                subTotal-=discount
                total=float("%.2f" %(subTotal))
            rendered= render_template('customers/pdf.html',customer=customer,orders=orders,invoice=invoice,total=total) 
            pdf = pdfkit.from_string(rendered,False)
            response=make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='inline : filename='+invoice+'.pdf'
            return response
    return (redirect(url_for('orders')))