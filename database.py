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
    customer["date_of_birth"] = fake.date_of_birth()
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


