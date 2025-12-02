import duckdb
from backend.storage.db import get_db_connection
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def detect_fraud():
    conn = get_db_connection()
    
    try:
        # Rule 1: High Value Transactions (> $800)
        # In a real system, we'd flag only new ones. Here we just query recent ones.
        high_value_query = """
        SELECT transaction_id, amount, timestamp 
        FROM transactions 
        WHERE amount > 800 
        AND timestamp > now() - INTERVAL 1 MINUTE
        """
        
        high_value_txs = conn.execute(high_value_query).fetchall()
        
        for tx in high_value_txs:
            tx_id, amount, ts = tx
            # Check if already flagged
            exists = conn.execute("SELECT COUNT(*) FROM fraud_alerts WHERE transaction_id = ?", (tx_id,)).fetchone()[0]
            if exists == 0:
                conn.execute("""
                    INSERT INTO fraud_alerts (transaction_id, reason, severity, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (tx_id, f"High Value Transaction: ${amount}", "HIGH", datetime.now()))
                logger.warning(f"Fraud Alert: High Value {tx_id}")

        # Rule 2: Rapid Transactions (More than 3 in 10 seconds for same buyer)
        # This is hard to simulate perfectly with random data, but let's try a query
        rapid_tx_query = """
        SELECT buyer_id, COUNT(*) as count
        FROM transactions
        WHERE timestamp > now() - INTERVAL 10 SECOND
        GROUP BY buyer_id
        HAVING count > 3
        """
        
        rapid_buyers = conn.execute(rapid_tx_query).fetchall()
        for buyer in rapid_buyers:
            buyer_id, count = buyer
            # Flag the latest transaction for this buyer
            latest_tx = conn.execute("SELECT transaction_id FROM transactions WHERE buyer_id = ? ORDER BY timestamp DESC LIMIT 1", (buyer_id,)).fetchone()
            if latest_tx:
                tx_id = latest_tx[0]
                exists = conn.execute("SELECT COUNT(*) FROM fraud_alerts WHERE transaction_id = ?", (tx_id,)).fetchone()[0]
                if exists == 0:
                    conn.execute("""
                        INSERT INTO fraud_alerts (transaction_id, reason, severity, timestamp)
                        VALUES (?, ?, ?, ?)
                    """, (tx_id, f"Rapid Transactions: {count} in 10s", "MEDIUM", datetime.now()))
                    logger.warning(f"Fraud Alert: Rapid Txs for {buyer_id}")

    except Exception as e:
        logger.error(f"Error in fraud detection: {e}")
    finally:
        conn.close()
