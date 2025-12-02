import random
from datetime import datetime
from faker import Faker
from backend.storage.models import ConsumerBehavior, Transaction, PublicData, FintechData

fake = Faker()

# Create a pool of users to ensure data overlaps
USER_POOL = [fake.uuid4() for _ in range(50)]
PARTNER_POOL = [fake.uuid4() for _ in range(5)]

class DataGenerator:
    def generate(self):
        raise NotImplementedError

class ConsumerBehaviorGenerator(DataGenerator):
    def generate(self) -> ConsumerBehavior:
        event_types = ['relocation', 'bill_payment', 'money_transfer', 'purchase', 'wealth_management']
        return ConsumerBehavior(
            user_id=random.choice(USER_POOL),
            timestamp=datetime.now(),
            event_type=random.choice(event_types),
            amount=round(random.uniform(10.0, 5000.0), 2),
            details={"location": fake.city(), "merchant": fake.company()}
        )

class TransactionGenerator(DataGenerator):
    def generate(self) -> Transaction:
        categories = ['electronics', 'clothing', 'home', 'books', 'grocery']
        return Transaction(
            transaction_id=fake.uuid4(),
            seller_id=fake.uuid4(),
            buyer_id=random.choice(USER_POOL),
            timestamp=datetime.now(),
            amount=round(random.uniform(5.0, 1000.0), 2),
            item_category=random.choice(categories)
        )

class PublicDataGenerator(DataGenerator):
    def generate(self) -> PublicData:
        return PublicData(
            citizen_id=random.choice(USER_POOL),
            criminal_record=random.choice([True, False]),
            academic_score=random.randint(50, 100),
            citizenship_status=random.choice(['citizen', 'resident', 'visa_holder']),
            last_updated=datetime.now()
        )

class FintechDataGenerator(DataGenerator):
    def generate(self) -> FintechData:
        return FintechData(
            partner_id=random.choice(PARTNER_POOL),
            user_id=random.choice(USER_POOL),
            credit_score_contributor=random.randint(300, 850),
            loan_history={"loans": random.randint(0, 5), "defaults": random.randint(0, 1)},
            timestamp=datetime.now()
        )
