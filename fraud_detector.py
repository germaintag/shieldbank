import sqlite3

def get_all_transactions():
    """Fetches all transactions from the database."""
    #Connect to the database and create a cursor
    connexion = sqlite3.connect("shieldbank.db")
    connexion.row_factory = sqlite3.Row
    cursor = connexion.cursor()

    #Run the SELECT query
    query = """
    SELECT bank_transaction.*, account.account_balance
    FROM bank_transaction 
    INNER JOIN account ON bank_transaction.account_id = account.account_id;
    """
    cursor.execute(query)
    #Fetch all raw rows
    raw_transactions = cursor.fetchall()
    connexion.close()
    #Convert each row into a dictionary
    #Step A: Empty list to store clean transactions
    clean_transactions = []
    #Step B: Loop through each raw row
    for row in raw_transactions:
        #Convert SQL row to Python dictionary
        formatted_row = dict(row)
        #Add dictionary to the clean list
        clean_transactions.append(formatted_row)
    #Step C: return the final list
    return clean_transactions

def check_insufficient_funds(transaction):
    """Checks if the transaction amount exceeds the available account balance."""
    #1 If it's a deposit, no alert
    if transaction["transaction_type"] == "deposit":
        return False
    #2 If the amount is greater than the balance, trigger alert
    if transaction["transaction_amount"] > transaction["account_balance"]:
        return True
    #3 Otherwise (amount <= balance), everything is fine
    else:
        return False

def check_contactless_limit(transaction):
    """Checks if a contactless payment exceeds the maximum limit of 50€."""
    return transaction["transaction_type"] == "contactless" and transaction["transaction_amount"] > 50.0

def check_high_amount(transaction):
    """Checks if the transaction amount exceeds the high-value threshold of 3000€."""
    return transaction["transaction_amount"] > 3000

def check_suspicious_hours(transaction):
    """Checks if the transaction time falls within suspicious night hours (01:00:00 to 05:00:00)."""
    return "01:00:00" <= transaction["transaction_time"] <= "05:00:00"

def run_fraud_detection():
    """Fetches all transactions and runs them through each fraud detection rule."""
