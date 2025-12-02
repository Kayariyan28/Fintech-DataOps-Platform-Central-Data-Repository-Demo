from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ConsumerBehavior(BaseModel):
    user_id: str
    timestamp: datetime
    event_type: str
    amount: float
    details: Dict[str, Any]

class Transaction(BaseModel):
    transaction_id: str
    seller_id: str
    buyer_id: str
    timestamp: datetime
    amount: float
    item_category: str

class PublicData(BaseModel):
    citizen_id: str
    criminal_record: bool
    academic_score: int
    citizenship_status: str
    last_updated: datetime

class FintechData(BaseModel):
    partner_id: str
    user_id: str
    credit_score_contributor: int
    loan_history: Dict[str, Any]
    timestamp: datetime

class CreditScore(BaseModel):
    user_id: str
    score: int
    last_updated: datetime
    factors: Dict[str, Any]
