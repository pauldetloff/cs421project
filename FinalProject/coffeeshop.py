from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
import os

app = Flask(__name__)
app.secret_key = "hello"
#using this video to help get db running https://www.youtube.com/watch?v=uZnp21fu8TQ&ab_channel=TechWithTim
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqllite3'
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False

db=SQLAlchemy(app)

#USER NAME JUST MADE SOME RANDOM ONE TO GET IT TO WORK WITH THAN KYOU PAGE AND ADDING ORDERS


#-----------------------------------------------------------------------------------------------------------
#                                         creating classes for each db 
#-----------------------------------------------------------------------------------------------------------

class Food(db.Model):
    __tablename__="foods"
    
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text)
    inventory= db.Column(db.Integer)
    price= db.Column(db.Float)
    
    def __init__(self,name,inventory,price):
        self.name=name
        self.inventory=inventory
        self.price=price
        
    def __repr__(self):
        return f"item {self.name} has {self.inventory} units and costs {self.price}"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #@isManager = db.Column(db.Integer, nullable=False)
    
    def __init__(self,username,password):
        self.username=username
        self.password=password
        #self.isManager=isManager

    def __repr__(self):
        return f'<User {self.username}>'
    
class Orders(db.Model):
    __tablename__="orders"
    
    id= db.Column(db.Integer, primary_key=True)
    uName= db.Column(db.Text)
    amountHotCoffee= db.Column(db.Integer)
    amountIcedCoffee= db.Column(db.Integer)
    amountBagel= db.Column(db.Integer)
    amountMocha= db.Column(db.Integer)
    saleTotal= db.Column(db.Float)
    
    def __init__(self,uName,amountHotCoffee,amountIcedCoffee,amountBagel,amountMocha,saleTotal):
        self.uName=uName
        self.amountHotCoffee=amountHotCoffee
        self.amountIcedCoffee=amountIcedCoffee
        self.amountBagel=amountBagel
        self.amountMocha=amountMocha
        self.saleTotal=saleTotal
    
    def __repr__(self):
        return f"{self.uName} ordered {self.amountHotCoffee} Hot Coffee, {self.amountIcedCoffee} Iced Coffee, {self.amountBagel}Bagel, and {self.amountMocha} Mocha. Total is ${self.saleTotal}."
    
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
#-----------------------------------------------------------------------------------------------------------
#                                         creating db and adding foods
#-----------------------------------------------------------------------------------------------------------

with app.app_context():
    db.create_all()
    

hotCoffee = Food('Hot Coffee',35,1.75)
icedCoffee = Food('Iced Coffee',33,2.50)
bagel = Food('Bagel',121,2.00)
mocha = Food('Mocha',12,4.25)
bBelcher = User("bBelcher","password123")

with app.app_context():
    Food.query.delete() #this clears the database bc it won't remove all the items from prior sessions
    Orders.query.delete()
    User.query.delete()
    db.session.add_all([hotCoffee,icedCoffee,bagel,mocha])
    db.session.add_all([bBelcher])
    db.session.commit()

    
   


@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('startHere.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    with app.app_context():
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            if not User.query.filter_by(username=username).first():
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                flash('Sign up successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already taken. Please choose a different one.', 'error')
        session.pop('_flashes', None)
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        global username
        username = form.username.data
        global manager
        #boolean value inverted. 0 means manager and 1 means not manager. careful! 
        if(username=="bBelcher"):
            manager=0
        else:
            manager=1
        password = form.password.data

        user = User.query.filter_by(username=username, password=password).first()

        if user is not None:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    session.pop('_flashes', None)
    return render_template('login.html', form=form)

@app.route('/home')
def home():
    return render_template('home.html',manager=manager)

@app.route('/menu')
def menu():
    #------------------ this will read the current db and set it up for html use
    itemNames=[]
    itemPrices=[]
    orderAmounts=[]
    with app.app_context():
        numberItems=Food.query.count()
        for i in range(1,numberItems+1):
            currentItem=Food.query.get(i)
            itemNames.append(currentItem.name)
            itemPrices.append(currentItem.price)
            orderAmounts.append(0)
            
    return render_template('menu.html',manager=manager,itemNames=itemNames,numberItems=numberItems,itemPrices=itemPrices)

@app.route('/thankyou')
def thankyou():
    orderTotal=0
    itemNames=[]
    itemPrices=[]
    orderAmounts=[]
    itemInventory=[]
    with app.app_context():
        numberItems=Food.query.count()
        for i in range(1,numberItems+1):
            currentItem=Food.query.get(i)
            itemNames.append(currentItem.name)
            itemPrices.append(currentItem.price)
            orderAmounts.append(0)
            itemInventory.append(currentItem.inventory)
    orderAmounts[0]=int(request.args.get('Hot Coffee'))
    orderAmounts[1]=int(request.args.get('Iced Coffee'))
    orderAmounts[2]=int(request.args.get('Bagel'))
    orderAmounts[3]=int(request.args.get('Mocha')) 
    for i in range(4):
        orderTotal=orderTotal+float(orderAmounts[i])*float(itemPrices[i])
    with app.app_context():
        order1 = Orders(username,orderAmounts[0],orderAmounts[1],orderAmounts[2],orderAmounts[3],orderTotal)
        db.session.add_all([order1])
        for i in range(1, numberItems+1):
            currentItem=Food.query.get(i)
            currentItem.inventory = currentItem.inventory - orderAmounts[i-1]
        db.session.commit()
    return render_template('thankyou.html',manager=manager,orderTotal=orderTotal)

@app.route('/orders')
def orders():
    numberOrders=Orders.query.count()
    theseOrders = Orders.query.all()
    return render_template('orders.html',manager=manager,numberOrders=numberOrders,theseOrders=theseOrders)

@app.route('/inventory')
def inventory():
    #------------------ this will read the current db and set it up for html use
    itemNames=[]
    itemPrices=[]
    orderAmounts=[]
    itemInventory=[]
    with app.app_context():
        numberItems=Food.query.count()
        for i in range(1,numberItems+1):
            currentItem=Food.query.get(i)
            itemNames.append(currentItem.name)
            itemPrices.append(currentItem.price)
            itemInventory.append(currentItem.inventory)
            orderAmounts.append(0)
    return render_template('inventory.html',manager=manager,itemNames=itemNames,numberItems=numberItems,itemPrices=itemPrices,itemInventory=itemInventory)

@app.route('/updatedInventory')
def updatedInventory():
    itemNames=[]
    itemPrices=[]
    itemInventory=[]
    numberItems=Food.query.count()
    itemPrices.append(float(request.args.get('Hot Coffee price')))
    itemPrices.append(float(request.args.get('Iced Coffee price')))
    itemPrices.append(float(request.args.get('Bagel price')))
    itemPrices.append(float(request.args.get('Mocha price')))
    itemInventory.append(int(request.args.get('Hot Coffee amount')))
    itemInventory.append(int(request.args.get('Iced Coffee amount')))
    itemInventory.append(int(request.args.get('Bagel amount')))
    itemInventory.append(int(request.args.get('Mocha amount')))
    with app.app_context():
        for i in range(1, numberItems+1):
            currentItem=Food.query.get(i)
            currentItem.inventory = itemInventory[i-1]
            currentItem.price = itemPrices[i-1]
        db.session.commit()
    return render_template('updatedInventory.html',manager=manager)

if __name__ == '__main__':
    app.run(debug=True)