from pydantic import BaseModel
from datetime import datetime

class PaddleSubscription(BaseModel):
    subscription_id: str
    next_billed_at: datetime | None
    cancellation_effective_at: datetime
    update_url: str
    cancel_url: str

class PaddlePrice(BaseModel):
    price_id: str
    name: str
    description: str
    amount: str
    currency: str
    product_id: str