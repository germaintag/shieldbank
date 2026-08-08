from faker import Faker
from database import (
    initializes_customers,
    add_one_customers,
    create_account_for_customer,
    generate_bank_transaction,
    insert_bank_transaction,
)

fake = Faker()
# Prompt user for the number of customer profiles to generate
number_of_customer = int(input("How many customer do you want to add to the database"))
# Populate database with linked Customer -> Account -> Transaction entities
for i in range(number_of_customer):
    #Generate and persist new customer profile
    customer = {}
    customer = initializes_customers(customer)
    customer_id = add_one_customers(customer)
    #Provision a bank account with initial balance for the customer
    account_id = create_account_for_customer(customer_id)
    #Simulate and record an initial bank transaction linked to the account
    transaction = {}
    transaction = generate_bank_transaction(transaction)
    insert_bank_transaction(transaction, account_id)