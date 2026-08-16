#  ShieldBank - Fraud Detection System

An automated Python and SQLite application designed to simulate banking activities, populate relational datasets with synthetic customer transactions, and detect potential financial fraud using configurable business rules.

---

## Project Overview

ShieldBank models a realistic banking infrastructure to detect suspicious behaviors in real time. It covers the end-to-end data lifecycle:
1. **Data Generation**: Generates synthetic client identities, accounts, and financial transactions.
2. **Relational Storage**: Persists data inside a normalized SQLite database with foreign keys and constraints.
3. **Rule-Based Detection**: Evaluates each transaction against a security rule engine.
4. **Terminal Reporting**: Aggregates and displays detailed alerts directly in the console.

---

##  Fraud Detection Rules

| Rule | Trigger Condition | Severity / Impact |
| :--- | :--- | :--- |
| **Insufficient Funds** | Transaction amount exceeds current account balance (excluding deposits) | Overdraft prevention |
| **Contactless Limit** | Contactless payment exceeding `50.00 EUR` | Payment standard breach |
| **High Value Amount** | Any single transaction exceeding `3,000.00 EUR` | Unusual transaction spike |
| **Suspicious Hours** | Transactions executed between `01:00:00` and `05:00:00` | High-risk time window |

---

##Database Schema

The database `shieldbank.db` contains four related tables:

* `customers`: Stores demographic data (`surname`, `forename`, `address`, `birthdate`, etc.).
* `account`: Stores financial balances linked to each customer (`customer_id`).
* `bank_transaction`: Records all operations (`deposit`, `withdrawal`, `transfer`, `payment`, `contactless`).
* `alert`: Logs triggered flags linked directly to the suspicious transaction (`transaction_id`).

---

## Project Structure

```text
├── database.py         # Database connection, queries, and table operations
├── generator.py        # Faker data generation logic for customers and accounts
├── fraud_detector.py   # Detection rules, engine orchestration, and CLI report
├── shieldbank.db       # SQLite database file
├── README.md           # Project documentation
└── requirements.txt    # External dependencies (Faker)