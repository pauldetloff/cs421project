import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key="hello"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

db=SQLAlchemy(app)

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