from flask import Flask, render_template, request
app = Flask (__name__)

manager = 1

@app.route('/')
def index():
    return render_template('home.html',manager=manager)

@app.route('/menu')
def menu():
    return render_template('menu.html',manager=manager)

@app.route('/cart')
def cart():
    return render_template('cart.html',manager=manager)

@app.route('/orders')
def orders():
    return render_template('orders.html',manager=manager)

@app.route('/inventory')
def inventory():
    return render_template('inventory.html',manager=manager)

if __name__ == '__main__':
    app.run(debug=True)