from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
#using this video to help get db running https://www.youtube.com/watch?v=uZnp21fu8TQ&ab_channel=TechWithTim
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqllite3'
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False

db=SQLAlchemy(app)

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
    
class People(db.Model):
    __tablename__="people"
    
    id= db.Column(db.Integer, primary_key=True)
    uName= db.Column(db.Text)
    pWord= db.Column(db.Text)
    isManager= db.Column(db.Integer)
    
    def __init__(self,uName,pWord,isManager):
        self.uName=uName
        self.pWord=pWord
        self.isManager=isManager
        
    def __repr__(self):
        return f"{self.uName}, {self.pWord}, {self.isManager}."
    
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
        return f"{self.uName}, {self.amountHotCoffee}, {self.amountIcedCoffee}, {self.amountBagel}, {self.amountMocha}, {self.saleTotal}."
    
#-----------------------------------------------------------------------------------------------------------
#                                         creating db and adding foods
#-----------------------------------------------------------------------------------------------------------

with app.app_context():
    db.create_all()
    

hotCoffee = Food('Hot Coffee',35,1.75)
icedCoffee = Food('Iced Coffee',33,2.50)
bagel = Food('Bagel',121,2.00)
mocha = Food('Mocha',12,4.25)
bBelcher = People("bBelcher","password123",1)
order1= Orders("bBelcher",0,0,1,2,1.25)

with app.app_context():
    Food.query.delete() #this clears the database bc it won't remove all the items from prior sessions
    People.query.delete()
    Orders.query.delete()
    #print(Food.query.count()) #this gives the count of all the foods in the database at the moment
    db.session.add_all([hotCoffee,icedCoffee,bagel,mocha])
    db.session.add_all([bBelcher])
    db.session.add_all([order1])
    db.session.commit()
    #print(hotCoffee)
    #print(Food.query.all())
    #hotCoffee.price = 2.00
    #db.session.commit()
    #print(hotCoffee)
    #print(Food.query.count()) #this gives the count of all the foods in the database at the moment
    #print("---------------------------")
    #print(People.query.all())
    #print("---------------------------")
    #print(Orders.query.all())
    #print(icedCoffee.name)
    #print(bagel.name)
    #print(mocha.name)

    
#boolean value inverted. 0 means manager and 1 means not manager. careful!    
manager = 0
username="sampleUser"


@app.route('/')
def index():
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
        print(itemNames)
        print(itemPrices)
        print(orderAmounts)
            
    return render_template('menu.html',manager=manager,itemNames=itemNames,numberItems=numberItems,itemPrices=itemPrices)

@app.route('/thankyou')
def thankyou():
    orderTotal=0
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
    orderAmounts[0]=int(request.args.get('Hot Coffee'))
    orderAmounts[1]=int(request.args.get('Iced Coffee'))
    orderAmounts[2]=int(request.args.get('Bagel'))
    orderAmounts[3]=int(request.args.get('Mocha'))
    for i in range(4):
        orderTotal=orderTotal+float(orderAmounts[i])*float(itemPrices[i])
    return render_template('thankyou.html',manager=manager,orderTotal=orderTotal)

@app.route('/orders')
def orders():
    return render_template('orders.html',manager=manager)

@app.route('/inventory')
def inventory():
    return render_template('inventory.html',manager=manager)

if __name__ == '__main__':
    app.run(debug=True)