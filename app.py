from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config

#Initialise Flask app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#Model for the 'customer' table
class customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True)

    phone_number = db.Column(db.String(20))
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    zip = db.Column(db.String(20))
    preffered_genre = db.Column(db.String(100))
    premium = db.relationship('premium_customer', uselist = False, back_populates = 'customer')
    regular = db.relationship('regular_customer', uselist = False, back_populates = 'customer')
    orders = db.relationship('customer_order', back_populates = 'customer')

class artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # <-- add autoincrement
    artist_name = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    products = db.relationship('artist_product', back_populates='artist')



class product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key = True)
    product_title = db.Column(db.String(255), nullable= False)
    price = db.Column(db.Numeric(10, 2), nullable = False)
    genre = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    media = db.Column(db.String(50))
    in_stock = db.Column(db.Integer, default=0)

    album = db.relationship('album', uselist = False, back_populates = 'product')
    single = db.relationship('single', uselist = False, back_populates = 'product')
    artists = db.relationship('artist_product', back_populates = 'product')
    tracks = db.relationship('product_track', back_populates = 'product')
    orders = db.relationship('order_product', back_populates = 'product')

class album(db.Model):
    __tablename__ = 'album'
    product = db.relationship('product', back_populates='album')
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete = 'CASCADE'), primary_key = True)
    album_type = db.Column(db.String(50))
    total_tracks = db.Column(db.Integer)

class single(db.Model):
    __tablename__ = 'single'
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete = 'CASCADE'), primary_key = True)
    bside_track = db.Column(db.String(255))
    radio_edit = db.Column(db.Boolean, default = False)
    product = db.relationship('product', back_populates='single')

class track(db.Model):
    __tablename__ = 'track'
    track_id = db.Column(db.Integer, primary_key = True)
    track_title = db.Column(db.String(255))
    length = db.Column(db.Time)
    products = db.relationship('product_track', back_populates = 'track')

class premium_customer(db.Model):
    __tablename__ = 'premium_customer'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id', ondelete = 'CASCADE'), primary_key = True)
    membership_level = db.Column(db.String(50))
    discount_rate = db.Column(db.Numeric(5, 2))
    join_date = db.Column(db.Date)
    customer = db.relationship('customer', back_populates = 'premium')

class regular_customer(db.Model):
    __tablename__ = 'regular_customer'
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.customer_id', ondelete = 'CASCADE'), primary_key = True)
    loyalty_points = db.Column(db.Integer, default = 0)
    newsletter_subscription = db.Column(db.Boolean, default = False)
    customer = db.relationship('customer', back_populates='regular')


class customer_order(db.Model):
    __tablename__ = 'customer_order'
    order_id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.customer_id'), nullable = False)
    order_date = db.Column(db.Date, nullable = False)
    filled = db.Column(db.Boolean, default = False)
    total_amount = db.Column(db.Numeric(10, 2))
    customer = db.relationship('customer', back_populates = 'orders')
    products = db.relationship('order_product', back_populates = 'order')

class artist_product(db.Model):
    __tablename__ = 'artist_product'
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.artist_id'), primary_key = True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'), primary_key = True)
    role = db.Column(db.String(50))
    artist = db.relationship('artist', back_populates='products')
    product = db.relationship('product', back_populates = 'artists')

class product_track(db.Model):
    __tablename__ = 'product_track'
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'), primary_key = True)
    track_id = db.Column(db.Integer,db.ForeignKey('track.track_id'), primary_key = True)
    track_number = db.Column(db.Integer)
    product = db.relationship('product', back_populates = 'tracks')
    track = db.relationship('track', back_populates = 'products')

class order_product(db.Model):
    __tablename__ = 'order_product'
    order_id = db.Column(db.Integer,db.ForeignKey('customer_order.order_id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True)
    quantity = db.Column(db.Integer, default = 1)
    unit_price = db.Column(db.Numeric(10, 2))
    order = db.relationship('customer_order', back_populates = 'products')
    product = db.relationship('product', back_populates = 'orders')


@app.route('/')
def index():
    return render_template('index.html')

# Route for displaying all customers
@app.route('/customers')
def customers():
    customers = customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/orders')
def orders():
    orders= customer_order.query.all()
    return render_template('orders.html', orders=orders)

# Route for displaying all products
@app.route('/products')
def products():
    products_list = product.query.all()
    return render_template('products.html', products=products_list)


# Route for displaying all artists
@app.route('/artists')
def artists():
    artists_list = artist.query.all()
    return render_template('artists.html', artists=artists_list)

# route for the imprint page
@app.route('/imprint')
def imprint():
    return render_template('imprint.html')


# adding an input page 
@app.route('/input')
def input():
    return render_template("input.html")


# entity inputs
@app.route('/add_product', methods= ['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = product (
            product_title = request.form['product_title'],
            price = request.form['price'],
            genre = request.form['genre'],
            release_date = request.form['release_date'],        
            media = request.form['media'],
            in_stock = request.form['in_stock']
            )
        db.session.add(new_product)
        db.session.commit()
        return render_template('product_feedback.html', product = new_product)
    return render_template('product_input.html')

    
        
@app.route('/add_artist', methods=['GET', 'POST'])
def add_artist():    
    if request.method == 'POST':
        name = request.form['artist_name']
        notes = request.form['notes']
        new_artist = artist(artist_name=name, notes=notes)
        db.session.add(new_artist)
        db.session.commit()
        return render_template('artist_feedback.html', artist=new_artist)
    return render_template('artist_input.html')


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        new_customer = customer(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            street=request.form['street'],
            city=request.form['city'],
            zip=request.form['zip'],
            preffered_genre=request.form['preffered_genre']
        )
        db.session.add(new_customer)
        db.session.commit()
        return render_template('customer_feedback.html', customer=new_customer)
    return render_template('customer_input.html')


@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    customers = customer.query.all()
    if request.method == 'POST':
        new_order = customer_order(
            customer_id = request.form['customer_id'],
            order_date = request.form['order_date'],
            filled = request.form['filled'] == 'True'  
        )
        db.session.add(new_order)
        db.session.commit()
        return render_template('order_feedback.html', order=new_order)
    return render_template('order_input.html', customers=customers)

#relationships input routes
@app.route('/link_artist_product', methods=['GET', 'POST'])
def link_artist_product():
    
    artists = artist.query.all()
    products = product.query.all()

    if request.method == 'POST':
        artist_id = request.form.get('artist_id')
        product_id = request.form.get('product_id')
        role = request.form.get('role')

        new_link = artist_product(
            artist_id=artist_id,
            product_id=product_id,
            role=role
        )
        db.session.add(new_link)
        db.session.commit()

        selected_artist = artist.query.get(artist_id)
        selected_product = product.query.get(product_id)

        return render_template('produces_feedback.html',artist=selected_artist,product=selected_product)

    return render_template('produces_input.html', artists=artists, products=products)


@app.route('/link_order_product', methods=['GET', 'POST'])
def link_order_product():
    orders = customer_order.query.all()
    products = product.query.all()

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        unit_price = request.form.get('unit_price')

        new_link = order_product (
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        db.session.add(new_link)
        db.session.commit()

        selected_product = product.query.get(product_id)
        selected_order = customer_order.query.get(order_id)

        return render_template('order_product_feedback.html', product=selected_product, order=selected_order)
    return render_template('order_product.html',products=products, orders=orders)
    

if __name__ == '__main__':
    app.run(debug=True)