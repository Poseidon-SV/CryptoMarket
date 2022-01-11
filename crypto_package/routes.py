# from flask.helpers import flash
from flask_wtf import form
from werkzeug.utils import validate_arguments
from wtforms.validators import Email
from crypto_package import app
from flask import render_template, redirect, url_for, flash, request
from crypto_package.models import Currency, User, Market
from crypto_package.forms import RegisterForm, LoginForm, PurchaseCurrencyForm, SellCurrencyForm
from crypto_package import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    market = Market.query.all()
    return render_template("home.html", market = market)
    

@app.route('/market', methods = ['GET', 'POST'])
@login_required
def market_page():  

    purchase_form = PurchaseCurrencyForm()
    selling_form = SellCurrencyForm()
    if request.method == "POST":
        # Purchase
        purchased_currency = request.form.get('purchased_currency')
        purchased_currency_object = Currency.query.filter_by(name= purchased_currency).first() 
        if purchased_currency_object:
            if current_user.can_purchase(purchased_currency_object):
                purchased_currency_object.buy(current_user)                
                flash(f"Congratulation! Trading of {purchased_currency_object.name} has been successfully done for {purchased_currency_object.price}$.", category= "success")
            else:
                flash(f"Sorry!! You don't have enough budget to do trading successfully of {purchased_currency_object.name}..!", category= "danger")

         #Selling currency 
        sold_currency = request.form.get('owned_currency')
        sold_currency_object = Currency.query.filter_by(name = sold_currency).first()
        if sold_currency_object:
            if current_user.can_sell(sold_currency_object):
                sold_currency_object.sell(current_user)
                flash(f"Congratulation! Trading of {sold_currency_object.name} has been successfully done for {sold_currency_object.price}$.", category= "success")
            else:
                flash(f'Something went wrong with trading {sold_currency_object.name}..!', category= "danger" )

        
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Currency.query.filter_by(owner = None) #to purchase an item
        owned_currency = Currency.query.filter_by(owner = current_user.id)        
        return render_template('market.html', item = items, purchase_form = purchase_form, owned_currency= owned_currency, selling_form = selling_form)
        
    ''' [
        {'SNo':'1', 'Name': 'Bitcoin', 'Price': '$47,440.31', 'change' : '-1.17%'},
        {'SNo':'2', 'Name': 'Ethereum', 'Price': '$3,746.83', 'change': '+0.63%'},
        {'SNo':'3', 'Name': 'Binance Coin', 'Price': '$523.04', 'change': '+1.50%'},
        {'SNo':'4', 'Name': 'Tether', 'Price': '$1.00', 'change': '+0.03%'}        
    ]'''

        

@app.route('/registration',methods = ['GET', 'POST'])
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data, email = form.email.data, password = form.password1.data)    
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Success! Account has been created.. You are logged in as {user_to_create.username}', category= 'success')
        return redirect(url_for('market_page'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(err_msg, category= 'danger') #f'There was an error with creating a User: '
            
    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category= 'success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not matched! Please try again', category= 'danger')

    return render_template('login.html', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category= 'info')
    return redirect(url_for("home_page"))
