# Online-Banking 

This is a simple online banking system implemented using Flask and SQLite. It allows users to register, log in, deposit money, withdraw money, and send money to other users. The application maintains user accounts and transaction histories.

## Features

User registration and login
User session management
Deposit money
Withdraw money
Send money to other users
View transaction history

## Prerequisites

Python 3.x
Flask
Flask-SQLAlchemy

## Installation

Clone the repository:
bash
git clone https://github.com/JanakanDev/online-banking-system.git
cd online-banking-system

Create a virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:
bash
pip install flask flask_sqlalchemy

Set up the database and run the application:
bash
python app.py

## Usage

Open your web browser and navigate to http://127.0.0.1:5000/.

Register a new user account.

Log in with your account credentials.

Use the navigation options to deposit money, withdraw money, or send money to other users.

## Code Overview

app.py: The main application file containing the Flask routes and database models.
templates/: Folder containing HTML templates for the different pages.

## Flask Routes

/: Home page displaying user information and transaction history.

/login: Login page for user authentication.

/register: Registration page for creating a new user account.

/logout: Logout route to end the user session.

/deposit: Route for depositing money into the user's account.

/withdraw: Route for withdrawing money from the user's account.

/send_money: Route for sending money to another user's account.

## Database Models

User: Represents a user with attributes like id, username, account_number, pin, balance, and a relationship with transactions.
Transaction: Represents a transaction with attributes like id, date, type, amount, user_id, sender_account, and receiver_account.

## Security Note

The secret_key and other sensitive information should be securely managed and not hardcoded in the production environment.
PINs and other sensitive information should be stored securely using appropriate hashing mechanisms.

## ScreenShots:
![Screenshot 2024-07-09 161208](https://github.com/JanakanDev/Online-Banking/assets/94671784/d588248f-081b-4098-a8c8-963e27d20a26)
![Screenshot 2024-07-09 161257](https://github.com/JanakanDev/Online-Banking/assets/94671784/e31a5d9b-a4db-4713-87d9-55c55e8766ac)
![Screenshot 2024-07-09 161520](https://github.com/JanakanDev/Online-Banking/assets/94671784/677e6557-67ad-4bf9-a757-49fc57ae3ca7)
![Screenshot 2024-07-09 161627](https://github.com/JanakanDev/Online-Banking/assets/94671784/6ff24d09-8752-4080-b07a-5f91540098c9)



