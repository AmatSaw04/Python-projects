import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

# --- App Initialization ---
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sk_test_tR3PYbcVNZZ796tH88S4VQ2u")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///store.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Login Manager Setup ---
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# --- Stripe Configuration ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")


# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Store hashed passwords, not plain text
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), nullable=False)


# --- User Loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables and seeds them with initial data."""
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            sample_products = [
                Product(title="Laptop", description="A powerful laptop", price_cents=70000, image="https://via.placeholder.com/200"),
                Product(title="Headphones", description="Noise cancelling headphones", price_cents=15000, image="https://via.placeholder.com/200"),
                Product(title="Phone", description="Latest smartphone", price_cents=50000, image="https://via.placeholder.com/200"),
            ]
            db.session.bulk_save_objects(sample_products)
            db.session.commit()
            print("Database has been initialized and seeded.")
        else:
            print("Database already contains data. Skipped seeding.")


# --- Routes ---
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/cart")
def cart():
    cart_product_ids = session.get('cart', [])
    cart_products = Product.query.filter(Product.id.in_(cart_product_ids)).all()
    total_price_cents = sum(product.price_cents for product in cart_products)
    return render_template("cart.html", cart_products=cart_products, total_price=total_price_cents / 100,
                           stripe_key=STRIPE_PUBLISHABLE_KEY)


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []

    # Add product and redirect to the cart page
    if product_id not in session['cart']:
        session['cart'].append(product_id)
        session.modified = True  # Mark the session as modified
        flash("Item added to your cart!", "success")
    else:
        flash("Item is already in your cart.", "info")

    return redirect(url_for('cart'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "warning")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    cart_product_ids = session.get('cart', [])
    if not cart_product_ids:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart'))

    cart_products = Product.query.filter(Product.id.in_(cart_product_ids)).all()
    line_items = []
    for product in cart_products:
        line_items.append({
            "price_data": {
                "currency": "inr",
                "product_data": {"name": product.title},
                "unit_amount": product.price_cents,
            },
            "quantity": 1,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cart', _external=True),
        )
        # Clear cart after creating checkout session
        session['cart'] = []
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash("Something went wrong with the payment process.", "danger")
        return str(e)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)