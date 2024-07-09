from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = '5t5t5t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    pin = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_account = db.Column(db.String(20))
    receiver_account = db.Column(db.String(20))

@app.route('/')
def index():
    if 'account_number' in session:
        with app.app_context():
            user = User.query.filter_by(account_number=session['account_number']).first()
            if user:
                transactions = Transaction.query.filter_by(user_id=user.id).all()
                return render_template('home.html', user=user, transactions=transactions)
            else:
                session.pop('account_number', None)
                session.pop('user_id', None)
                return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form['account_number']
        pin = request.form['pin']
        user = User.query.filter_by(account_number=account_number, pin=pin).first()
        if user:
            session['account_number'] = account_number
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        account_number = request.form['account_number']
        pin = request.form['pin']
        user = User(username=username, account_number=account_number, pin=pin, balance=0.0)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('account_number', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'account_number' in session:
        amount = float(request.form['amount'])
        with app.app_context():
            user = User.query.filter_by(account_number=session['account_number']).first()
            if user:
                user.balance += amount
                transaction = Transaction(type='Credit', amount=amount, user_id=user.id, receiver_account=user.account_number)
                db.session.add(transaction)
                db.session.commit()
    return redirect(url_for('index'))


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'account_number' in session:
        amount = float(request.form['amount'])
        with app.app_context():
            user = User.query.filter_by(account_number=session['account_number']).first()
            if user and user.balance >= amount:
                user.balance -= amount
                transaction = Transaction(type='Debit', amount=amount, user_id=user.id, sender_account=user.account_number)
                db.session.add(transaction)
                db.session.commit()
    return redirect(url_for('index'))


@app.route('/send_money', methods=['POST'])
def send_money():
    if 'account_number' in session:
        recipient_account_number = request.form['recipient_account_number']
        amount = float(request.form['amount'])
        with app.app_context():
            user = User.query.filter_by(account_number=session['account_number']).first()
            recipient = User.query.filter_by(account_number=recipient_account_number).first()
            if user and recipient and user.balance >= amount:
                user.balance -= amount
                recipient.balance += amount
                transaction = Transaction(type='Send', amount=amount, user_id=user.id, sender_account=user.account_number, receiver_account=recipient.account_number)
                db.session.add(transaction)
                
                recipient_transaction = Transaction(type='Send', amount=amount, user_id=recipient.id, sender_account=user.account_number, receiver_account=recipient.account_number)
                db.session.add(recipient_transaction)
                
                db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
