import sqlite3
import random
from faker import Faker
fake = Faker()
def initializes_customers(customer):
    """
    Generates fake customer data using Faker and populates a dictionary.
    :param customer: A dictionary that will hold the generated customer data.
    :return: None
    """

    gender = ["M","F"]
    customer["surname"] = fake.last_name()
    customer["forename"] = fake.first_name()
    customer["sex"]= random.choice(gender)
    customer["date_of_birth"] = str(fake.date_of_birth())
    customer["street"] = fake.street_address()
    customer["city"] = fake.city()
    customer["postal_code"] = fake.postcode()
    customer["country"] = fake.country()
    return customer



def add_one_customers(customer):
    """
    Inserts a single customer dictionary record into the SQLite database.

    :param customer: A dictionary containing the customer's attributes
                     (surname, forename, sex, date_of_birth, street, city,
                     postal_code, country).
    :return: None
    """
    connexion = sqlite3.connect("shieldbank.db")
    cursor = connexion.cursor()
    # SQL query to insert customer data
    query = """
    INSERT INTO customers (surname, forename, sex, date_of_birth, street, city, postal_code, country)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    # Extract dictionary values
    values = (customer["surname"],customer["forename"], customer["sex"],customer["date_of_birth"],customer["street"],customer["city"],customer["postal_code"],customer["country"])
    # Execute insertion for this customer
    cursor.execute(query, values)
    connexion.commit()
    connexion.close()
    return cursor.lastrowid



def generate_amount():
    """Generates a single random account balance"""
    account_balance = float(fake.pydecimal(left_digits = 4, right_digits = 2, positive=True))
    return account_balance


def create_account_for_customer(customer_id):
    """Insert an account amount into the database."""
    client_id = customer_id
    connexion = sqlite3.connect("shieldbank.db")
    cursor = connexion.cursor()
    # SQL query to insert the amount
    query = """INSERT INTO account (account_balance, customer_id)VALUES (?, ?);"""
    amount = generate_amount()
    values = (amount, client_id)
    # Execute insertion for the amount
    cursor.execute(query, values)
    connexion.commit()
    connexion.close()
    return cursor.lastrowid


def generate_bank_transaction(transaction):
    """Generates a random type of transaction.
       :param transaction: A dictionary that will hold the transaction's attributes
    """
    the_type_of_transaction = ["deposit","withdrawal","transfer","payment","contactless"]
    transaction["transaction_amount"] = round(random.uniform(1.00, 5000.00),2)
    transaction["transaction_type"] = random.choice(the_type_of_transaction)
    transaction["transaction_date"] = str(fake.date_between(start_date="-1y", end_date="today"))
    transaction["transaction_time"] = fake.time()
    transaction["transaction_location"] = fake.city()
    return transaction



def insert_bank_transaction(transaction, account_id):
    """insert a bank_transaction type into the database."""
    connexion = sqlite3.connect("shieldbank.db")
    cursor = connexion.cursor()
    query = """INSERT INTO bank_transaction (transaction_type,transaction_amount, transaction_date, transaction_time, transaction_location, account_id)VALUES (?, ?, ?, ?, ?, ?);"""
    values = (transaction["transaction_type"], transaction["transaction_amount"],transaction["transaction_date"], transaction["transaction_time"], transaction["transaction_location"], account_id )
    cursor.execute(query, values)
    connexion.commit()
    connexion.close()
    return cursor.lastrowid

def add_alert(transaction,alert_type):
    """insert a bank_transaction type as an alert in  the database."""
    connexion = sqlite3.connect("shieldbank.db")
    cursor = connexion.cursor()
    query = """INSERT INTO alert (alert_type, transaction_id) VALUES (?, ?);"""
    values = (alert_type, transaction["transaction_id"])
    cursor.execute(query, values)
    connexion.commit()
    connexion.close()
    return cursor.lastrowid

def get_alerts_report():
    """Fetches all recorded fraud alerts joined with transaction,account, and customer details. """
    connexion = sqlite3.connect("shieldbank.db")
    connexion.row_factory = sqlite3.Row
    cursor = connexion.cursor()
    query = """
    SELECT 
        alert.alert_id,
        alert.alert_type,
        bank_transaction.transaction_id,
        bank_transaction.transaction_type,
        bank_transaction.transaction_amount,
        bank_transaction.transaction_date,
        bank_transaction.transaction_time,
        bank_transaction.transaction_location,
        account.account_id,
        account.account_balance,
        customers.surname,
        customers.forename
    FROM alert
    INNER JOIN bank_transaction ON alert.transaction_id = bank_transaction.transaction_id
    INNER JOIN account ON bank_transaction.account_id = account.account_id
    INNER JOIN customers ON account.customer_id = customers.customer_id
    ORDER BY alert.alert_id ASC;
    """
    cursor.execute(query)
    #Convert rows to dictionaries step by step
    rows = cursor.fetchall()
    alerts = []
    for row in rows:
        alert_dict = dict(row)
        alerts.append(alert_dict)
    connexion.close()
    return alerts
