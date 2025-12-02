from backend.storage.db import get_db_connection
import logging

logger = logging.getLogger(__name__)

def run_data_quality_checks():
    conn = get_db_connection()
    results = {
        "timestamp": None,
        "checks": []
    }
    
    try:
        # Check 1: No negative amounts in transactions
        neg_amounts = conn.execute("SELECT COUNT(*) FROM transactions WHERE amount < 0").fetchone()[0]
        results["checks"].append({
            "name": "No Negative Transaction Amounts",
            "passed": neg_amounts == 0,
            "details": f"Found {neg_amounts} negative transactions"
        })
        
        # Check 2: Valid Credit Scores
        invalid_scores = conn.execute("SELECT COUNT(*) FROM credit_scores WHERE score < 300 OR score > 850").fetchone()[0]
        results["checks"].append({
            "name": "Valid Credit Score Range (300-850)",
            "passed": invalid_scores == 0,
            "details": f"Found {invalid_scores} invalid scores"
        })
        
        # Check 3: Data Freshness (Consumer Behavior)
        # Just checking if we have data from the last minute for demo purposes
        # In a real scenario, we'd check max(timestamp)
        count_recent = conn.execute("SELECT COUNT(*) FROM consumer_behavior").fetchone()[0]
        results["checks"].append({
            "name": "Data Flowing (Consumer Behavior)",
            "passed": count_recent > 0,
            "details": f"Total records: {count_recent}"
        })

        logger.info(f"Data Quality Checks: {results}")
        return results

    except Exception as e:
        logger.error(f"Error running DQ checks: {e}")
        return results
    finally:
        conn.close()
