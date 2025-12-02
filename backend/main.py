from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.ingestion.manager import IngestionManager
from backend.processing.credit_scoring import calculate_credit_scores
from backend.processing.profiling import run_data_quality_checks
from backend.processing.fraud_detection import detect_fraud
from backend.storage.db import get_db_connection, init_db
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DataOps Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
ingestion_manager = IngestionManager()
processing_scheduler = BackgroundScheduler()

@app.on_event("startup")
def startup_event():
    init_db()
    # Schedule credit scoring every 10 seconds
    processing_scheduler.add_job(calculate_credit_scores, 'interval', seconds=10)
    # Schedule fraud detection every 5 seconds
    processing_scheduler.add_job(detect_fraud, 'interval', seconds=5)
    processing_scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    ingestion_manager.stop()
    processing_scheduler.shutdown()

@app.post("/pipeline/start")
def start_pipeline():
    try:
        ingestion_manager.start()
        return {"status": "Pipeline started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pipeline/stop")
def stop_pipeline():
    ingestion_manager.stop()
    return {"status": "Pipeline stopped"}

@app.get("/pipeline/status")
def get_pipeline_status():
    # In a real app, we'd check the actual scheduler state
    return {
        "ingestion_running": ingestion_manager.scheduler.running,
        "processing_running": processing_scheduler.running
    }

@app.get("/dataops/metrics")
def get_metrics():
    return run_data_quality_checks()

@app.get("/data/consumer")
def get_consumer_data(limit: int = 50):
    conn = get_db_connection()
    df = conn.execute(f"SELECT * FROM consumer_behavior ORDER BY timestamp DESC LIMIT {limit}").df()
    conn.close()
    return df.to_dict(orient="records")

@app.get("/data/transactions")
def get_transaction_data(limit: int = 50):
    conn = get_db_connection()
    df = conn.execute(f"SELECT * FROM transactions ORDER BY timestamp DESC LIMIT {limit}").df()
    conn.close()
    return df.to_dict(orient="records")

@app.get("/data/scores")
def get_credit_scores(limit: int = 50):
    conn = get_db_connection()
    df = conn.execute(f"SELECT * FROM credit_scores ORDER BY last_updated DESC LIMIT {limit}").df()
    conn.close()
    return df.to_dict(orient="records")

@app.get("/data/fraud-alerts")
def get_fraud_alerts(limit: int = 50):
    conn = get_db_connection()
    df = conn.execute(f"SELECT * FROM fraud_alerts ORDER BY timestamp DESC LIMIT {limit}").df()
    conn.close()
    return df.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
