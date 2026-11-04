# ShieldBank - Fraud Detection & SQL Risk Analytics

An end-to-end banking compliance project built with Python, SQLite, and SQL.  
It simulates financial operations, detects fraud patterns via a rule engine, and provides SQL audit queries for Anti-Money Laundering (AML) surveillance.

---

## Business Context & SQL Audit Queries

The core analytical logic is located in `analysis.sql`. It answers critical risk and compliance questions:

| # | Business Goal (Risk & Compliance) | SQL Analytical Approach |
| :--- | :--- | :--- |
| **1** | **Financial Flow Profiling**: Compare volume and ticket sizes across payment channels to establish cash flow baselines. | Aggregations (`COUNT`, `AVG`, `MIN`, `MAX`) grouped by channel, sorted by highest average amount. |
| **2** | **High-Risk AML Customers**: Identify customers triggering repeated suspicious alerts (priority compliance list). | Multi-table relational joins (`INNER JOIN`) filtered with `HAVING alert_count >= 2`. |
| **3** | **Channel Vulnerability Matrix**: Measure incident frequency per payment method, including secure zero-alert channels. | Preserved channels using `LEFT JOIN` and accurate key counting (`COUNT(alert_id)`). |
| **4** | **Transaction Volume Tiering**: Segment operations into Low (<50€), Medium (50–1000€), and High (>1000€) brackets. | Conditional classification (`CASE WHEN`) aggregated dynamically via `GROUP BY`. |
| **5** | **Chronological Audit Trail**: Provide auditors with an ordered transaction history to trace rapid fund movements. | Hierarchical multi-level ordering (`ORDER BY customer_id, transaction_date`). |

---

## Fraud Detection Rules (Rule Engine)

Each generated transaction is evaluated against a business security engine before persistence:

| Rule | Trigger Condition | Banking Risk Managed |
| :--- | :--- | :--- |
| **Insufficient Funds** | Transaction exceeds current account balance (excluding deposits) | Overdraft prevention (`account_balance >= 0`) |
| **Contactless Limit** | Contactless payment exceeding `50.00 EUR` | Payment security standard breach |
| **High Value Amount** | Single transaction exceeding `3,000.00 EUR` | Unusual transaction spike |
| **Suspicious Hours** | Transactions executed between `01:00:00` and `05:00:00` | Off-hours fraud risk |
| **Location Anomaly** | Sudden geographical shift across successive operations | Geo-spoofing and card cloning risk |

---

## Relational Database Schema

The SQLite database (`shieldbank.db`) follows a 3NF normalized schema with strict integrity constraints (`FOREIGN KEY`, `CHECK`, `NOT NULL`):

- **`customers`** (Client Identity & Demographics)  
  `customer_id` (PK), `surname`, `forename`, `sex` (`CHECK IN ('F', 'M')`), `date_of_birth`, `street`, `city`, `postal_code`, `country`.

- **`account`** (Bank Accounts & Balances)  
  `account_id` (PK), `account_balance` (`CHECK (account_balance >= 0)`), `customer_id` (FK $\to$ `customers.customer_id`).

- **`bank_transaction`** (Operations Ledger)  
  `transaction_id` (PK), `transaction_type` (`CHECK IN ('deposit', 'withdrawal', 'transfer', 'payment', 'contactless')`), `transaction_amount`, `transaction_date`, `transaction_time`, `transaction_location`, `account_id` (FK $\to$ `account.account_id`).

- **`alert`** (Compliance & Security Flags)  
  `alert_id` (PK), `alert_type` (`CHECK IN ('insufficient_funds', 'contactless_limit_exceeded', 'suspicious_location_change', 'high_amount', 'suspicious_hours')`), `transaction_id` (FK $\to$ `bank_transaction.transaction_id`).

---

## Project Structure

```text
├── analysis.sql        # Documented SQL audit queries (AML, risk profiling, flows)
├── database.py         # Database connection helper and schema initialization
├── fraud_detector.py   # Security rule engine and alert logging logic
├── main.py             # Pipeline execution entry point
├── schema.sql          # DDL table creation and relational constraints
├── shieldbank.db       # Relational SQLite database
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation