/*
   Project: ShieldBank - SQL Risk & Compliance Analysis
   Author: Germain TAGODOE (L3 Data Project)
   Description: SQL queries on SQLite database (shieldbank.db) to analyze
                fraud alerts, transaction tiers, and suspicious accounts.
*/

-- 1. Financial summary by transaction type
-- Compare average amounts and volumes across payment methods
SELECT
      transaction_type,
      COUNT(transaction_id) AS transaction_count,
      ROUND(AVG(transaction_amount),2) AS avg_transaction_amount,
      MIN(transaction_amount) AS min_transaction_amount,
      MAX(transaction_amount) AS max_transaction_amount
FROM bank_transaction
GROUP BY transaction_type
ORDER BY avg_transaction_amount DESC;

-- 2. High-risk customers (AML monitoring)
-- Find customers with 2 or more fraud alerts
SELECT
      customer_id,
      surname,
      forename,
      COUNT(alert_id) AS alert_count
FROM customers
INNER JOIN account
USING(customer_id)
INNER JOIN bank_transaction
USING(account_id)
INNER JOIN alert
USING(transaction_id)
GROUP BY customer_id
HAVING alert_count >= 2;

-- 3. Alerts per payment method
-- Keep channels with 0 alerts using a LEFT JOIN
SELECT
      transaction_type,
      COUNT(alert_id) AS alert_count
FROM bank_transaction
LEFT JOIN  alert
USING(transaction_id)
GROUP BY transaction_type;

-- 4. Transaction volume segmentation
-- Split transactions into Low, Medium, and High tiers
SELECT
    CASE
        WHEN transaction_amount < 50 THEN 'Low'
        WHEN transaction_amount BETWEEN 50 AND 1000 THEN 'Medium'
        ELSE 'High'
    END AS amount_tier,
    COUNT(transaction_id) AS transaction_count
FROM bank_transaction
GROUP BY amount_tier;

-- 5. Customer transaction history
-- Chronological order per customer for compliance review
SELECT
      customer_id,
      surname,
      transaction_id,
      transaction_date,
      transaction_amount
FROM account
INNER JOIN bank_transaction
USING(account_id)
INNER JOIN customers
USING(customer_id)
ORDER BY customer_id,transaction_date;
