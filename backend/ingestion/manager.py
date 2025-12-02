from apscheduler.schedulers.background import BackgroundScheduler
from backend.ingestion.generators import ConsumerBehaviorGenerator, TransactionGenerator, PublicDataGenerator, FintechDataGenerator
from backend.storage.db import insert_consumer_behavior, insert_transaction, insert_public_data, insert_fintech_data
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.consumer_gen = ConsumerBehaviorGenerator()
        self.transaction_gen = TransactionGenerator()
        self.public_gen = PublicDataGenerator()
        self.fintech_gen = FintechDataGenerator()

    def ingest_consumer_data(self):
        data = self.consumer_gen.generate()
        insert_consumer_behavior(data)
        logger.info(f"Ingested Consumer Data: {data.user_id}")

    def ingest_transaction_data(self):
        data = self.transaction_gen.generate()
        insert_transaction(data)
        logger.info(f"Ingested Transaction Data: {data.transaction_id}")

    def ingest_public_data(self):
        data = self.public_gen.generate()
        insert_public_data(data)
        logger.info(f"Ingested Public Data: {data.citizen_id}")

    def ingest_fintech_data(self):
        data = self.fintech_gen.generate()
        insert_fintech_data(data)
        logger.info(f"Ingested Fintech Data: {data.partner_id}")

    def start(self):
        # Schedule jobs to run at different intervals to simulate realistic traffic
        self.scheduler.add_job(self.ingest_consumer_data, 'interval', seconds=2)
        self.scheduler.add_job(self.ingest_transaction_data, 'interval', seconds=1)
        self.scheduler.add_job(self.ingest_public_data, 'interval', seconds=5)
        self.scheduler.add_job(self.ingest_fintech_data, 'interval', seconds=3)
        self.scheduler.start()
        logger.info("Ingestion Manager started.")

    def stop(self):
        self.scheduler.shutdown()
        logger.info("Ingestion Manager stopped.")
