# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import stripe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donors.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['STRIPE_PUBLIC_KEY'] = 'your_stripe_public_key'
app.config['STRIPE_SECRET_KEY'] = 'your_stripe_secret_key'
db = SQLAlchemy(app)
stripe.api_key = app.config['STRIPE_SECRET_KEY']

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    school = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    donors = Donor.query.order_by(Donor.amount.desc()).all()
    return render_template('index.html', donors=donors)

@app.route('/donate', methods=['POST'])
def donate():
    amount = round(float(request.form['amount']) * 100)  # in cents
    customer = stripe.Customer.create(email=request.form['email'], source=request.form['stripeToken'])
    stripe.Charge.create(customer=customer.id, amount=amount, currency='usd', description='Donation')
    donor = Donor(name=request.form['name'], email=request.form['email'], school=request.form['school'], amount=amount)
    db.session.add(donor)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
