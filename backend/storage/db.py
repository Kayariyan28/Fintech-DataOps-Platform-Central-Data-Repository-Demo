import duckdb
import os

DB_PATH = "backend/data_repository.duckdb"

def get_db_connection():
    conn = duckdb.connect(DB_PATH)
    return conn

def init_db():
    conn = get_db_connection()
    
    # 1. Consumer Behavior
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS seq_consumer_id;
        CREATE TABLE IF NOT EXISTS consumer_behavior (
            id INTEGER DEFAULT nextval('seq_consumer_id'),
            user_id VARCHAR,
            timestamp TIMESTAMP,
            event_type VARCHAR,
            amount DOUBLE,
            details JSON,
            PRIMARY KEY (id)
        )
    """)
    
    # 2. Transaction Data
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS seq_transaction_id;
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER DEFAULT nextval('seq_transaction_id'),
            transaction_id VARCHAR,
            seller_id VARCHAR,
            buyer_id VARCHAR,
            timestamp TIMESTAMP,
            amount DOUBLE,
            item_category VARCHAR,
            PRIMARY KEY (id)
        )
    """)
    
    # 3. Public Data
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS seq_public_id;
        CREATE TABLE IF NOT EXISTS public_data (
            id INTEGER DEFAULT nextval('seq_public_id'),
            citizen_id VARCHAR,
            criminal_record BOOLEAN,
            academic_score INTEGER,
            citizenship_status VARCHAR,
            last_updated TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)
    
    # 4. Fintech Data
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS seq_fintech_id;
        CREATE TABLE IF NOT EXISTS fintech_data (
            id INTEGER DEFAULT nextval('seq_fintech_id'),
            partner_id VARCHAR,
            user_id VARCHAR,
            credit_score_contributor INTEGER,
            loan_history JSON,
            timestamp TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)

    # 5. Derived Credit Scores (The "Product" Output)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS credit_scores (
            user_id VARCHAR,
            score INTEGER,
            last_updated TIMESTAMP,
            factors JSON,
            PRIMARY KEY (user_id)
        )
    """)

    # 6. Fraud Alerts
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS seq_fraud_id;
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id INTEGER DEFAULT nextval('seq_fraud_id'),
            transaction_id VARCHAR,
            reason VARCHAR,
            severity VARCHAR,
            timestamp TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)
    
    conn.close()
    print("Database initialized successfully.")

def insert_consumer_behavior(data):
    conn = get_db_connection()
    conn.execute("INSERT INTO consumer_behavior (user_id, timestamp, event_type, amount, details) VALUES (?, ?, ?, ?, ?)",
                 (data.user_id, data.timestamp, data.event_type, data.amount, data.details))
    conn.close()

def insert_transaction(data):
    conn = get_db_connection()
    conn.execute("INSERT INTO transactions (transaction_id, seller_id, buyer_id, timestamp, amount, item_category) VALUES (?, ?, ?, ?, ?, ?)",
                 (data.transaction_id, data.seller_id, data.buyer_id, data.timestamp, data.amount, data.item_category))
    conn.close()

def insert_public_data(data):
    conn = get_db_connection()
    conn.execute("INSERT INTO public_data (citizen_id, criminal_record, academic_score, citizenship_status, last_updated) VALUES (?, ?, ?, ?, ?)",
                 (data.citizen_id, data.criminal_record, data.academic_score, data.citizenship_status, data.last_updated))
    conn.close()

def insert_fintech_data(data):
    conn = get_db_connection()
    conn.execute("INSERT INTO fintech_data (partner_id, user_id, credit_score_contributor, loan_history, timestamp) VALUES (?, ?, ?, ?, ?)",
                 (data.partner_id, data.user_id, data.credit_score_contributor, data.loan_history, data.timestamp))
    conn.close()

if __name__ == "__main__":
    init_db()
