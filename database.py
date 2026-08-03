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


def generate_amount():
    """Generates a single random account balance"""
    account_balance = fake.pydecimal(left_digits = 4, right_digits = 2, positive=True)
    return account_balance


def add_account_amount(customer_id):
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



def generate_bank_transaction(transaction):
    """Generates a random type of transaction.
       :param transaction: A dictionary that will hold the transaction's attributes
    """
    the_type_of_transaction = ["deposit","withdrawal","transfer","payment"]
    transaction["transaction_type"] = random.choice(the_type_of_transaction)
    transaction["transaction_date"] = str(fake.date_between(start_date="-1y", end_date="today"))
    transaction["transaction_time"] = fake.time()
    transaction["transaction_location"] = fake.city()



def add_bank_transaction(transaction, account_id):
    """insert a bank_transaction type into the database."""
    connexion = sqlite3.connect("shieldbank.db")
    cursor = connexion.cursor()
    query = """INSERT INTO bank_transaction (transaction_type, transaction_date, transaction_time, transaction_location, account_id)VALUES (?, ?, ?, ?, ?);"""
    values = (transaction["transaction_type"], transaction["transaction_date"], transaction["transaction_time"], transaction["transaction_location"], account_id )
    cursor.execute(query, values)
    connexion.commit()
    connexion.close()

