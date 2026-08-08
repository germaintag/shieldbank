CREATE TABLE customers(
   customer_id INTEGER PRIMARY KEY ,
   surname VARCHAR(10) NOT NULL ,
   forename VARCHAR(10) NOT NULL ,
   sex CHAR(1) CHECK(sex IN ('F','M')),
   date_of_birth DATE NOT NULL,
   street VARCHAR(150) NOT NULL,
   city VARCHAR(150) NOT NULL,
   postal_code VARCHAR(150) NOT NULL,
   country VARCHAR(150) NOT NULL
);

CREATE TABLE account(
   account_id INTEGER PRIMARY KEY ,
   account_balance REAL CHECK(account_balance >= 0),
   customer_id INTEGER REFERENCES customers(customer_id)
);

CREATE TABLE bank_transaction(
  transaction_id INTEGER PRIMARY KEY ,
  transaction_type VARCHAR(180) CHECK(transaction_type IN ("deposit","withdrawal","transfer","payment","contactless")),
  transaction_amount REAL NOT NULL ,
  transaction_date DATE NOT NULL ,
  transaction_time TIME NOT NULL ,
  transaction_location VARCHAR(50) NOT NULL,
  account_id INTEGER REFERENCES account(account_id)
);

CREATE TABLE alert(
  alert_id INTEGER PRIMARY KEY ,
  alert_type VARCHAR(50) CHECK(alert_type IN ('insufficient_funds','contactless_limit_exceeded','suspicious_location_change', 'high_amount', 'suspicious_hours')),
  transaction_id INTEGER REFERENCES bank_transaction (transaction_id)
);