import duckdb
import pandas as pd
from backend.storage.db import get_db_connection
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def calculate_credit_scores():
    conn = get_db_connection()
    
    # Simulate a "Spark" job by reading into Pandas/Arrow
    # Join Consumer Behavior, Transactions, and Fintech Data
    
    query = """
    SELECT 
        cb.user_id,
        COUNT(cb.id) as transaction_count,
        SUM(cb.amount) as total_spend,
        MAX(fd.credit_score_contributor) as external_score,
        MAX(fd.loan_history) as loan_history,
        MAX(pd.criminal_record) as has_criminal_record,
        MAX(pd.academic_score) as academic_score
    FROM consumer_behavior cb
    LEFT JOIN fintech_data fd ON cb.user_id = fd.user_id
    LEFT JOIN public_data pd ON cb.user_id = pd.citizen_id
    GROUP BY cb.user_id
    """
    
    try:
        df = conn.execute(query).df()
        
        if df.empty:
            logger.info("No data to process for credit scores.")
            conn.close()
            return

        # Enhanced scoring logic
        def compute_score(row):
            base_score = 300
            
            # 1. Criminal Record (Major Impact)
            if row['has_criminal_record']:
                return 300 
            
            score = base_score
            
            # 2. Transaction Activity (Up to 100 pts)
            score += min(row['transaction_count'] * 2, 100) 
            
            # 3. Spending Power (Up to 150 pts)
            score += min(row['total_spend'] / 100, 150) 
            
            # 4. External Fintech Score (Weighted 40%)
            if pd.notnull(row['external_score']):
                score += (row['external_score'] - 300) * 0.4
            
            # 5. Academic Performance (Up to 50 pts)
            if pd.notnull(row['academic_score']):
                score += (row['academic_score'] / 100) * 50
                
            # 6. Loan History (Penalty for defaults)
            if pd.notnull(row['loan_history']):
                try:
                    history = json.loads(row['loan_history']) if isinstance(row['loan_history'], str) else row['loan_history']
                    if history.get('defaults', 0) > 0:
                        score -= 100
                    score += min(history.get('loans', 0) * 10, 50) # Credit mix bonus
                except:
                    pass
            
            return min(max(int(score), 300), 850)

        df['final_score'] = df.apply(compute_score, axis=1)
        
        # Write back to DB
        for _, row in df.iterrows():
            factors = {
                "transaction_count": row['transaction_count'],
                "total_spend": round(row['total_spend'], 2),
                "external_score": row['external_score'] if pd.notnull(row['external_score']) else None,
                "academic_bonus": row['academic_score'] if pd.notnull(row['academic_score']) else 0,
                "loan_penalty": "Yes" if pd.notnull(row['loan_history']) and str(row['loan_history']).find('defaults') > 0 else "No"
            }
            
            conn.execute("""
                INSERT INTO credit_scores (user_id, score, last_updated, factors) 
                VALUES (?, ?, ?, ?)
                ON CONFLICT (user_id) DO UPDATE SET 
                    score = excluded.score,
                    last_updated = excluded.last_updated,
                    factors = excluded.factors
            """, (row['user_id'], row['final_score'], datetime.now(), json.dumps(factors)))
            
        logger.info(f"Updated credit scores for {len(df)} users.")
        
    except Exception as e:
        logger.error(f"Error calculating credit scores: {e}")
    finally:
        conn.close()
