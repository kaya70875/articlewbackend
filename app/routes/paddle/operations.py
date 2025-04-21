from app.models.database import db
from pymongo import ReturnDocument
from app.routes.paddle.utils import *

users_collection = db.get_collection('users')

def cancel_subscription(data: dict):
    """
    Updates canceled paddle subscription status to canceled.
    After this action user should still use the service until the end of the billing cycle.
    """

    try:        
        # Update the user's subscription status in the database

        customer_email = get_customer_email(data)
        users_collection.find_one_and_update(
            {"email": customer_email},
            {"$set": {"subscription_status": 'cancelled'}},
            return_document=ReturnDocument.AFTER
        )
    except Exception as e:
        print(f"Error handling subscription cancelled event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription cancelled event: {e}")

def reactivate_subscription(data: dict):
    """
    Reactivates the subscription status in the database.
    This function should be called when a subscription is reactivated.
    """

    try:
        # Get the customer email from Paddle
        customer_email = get_customer_email(data)

        # Update the user's subscription status in the database
        users_collection.find_one_and_update(
            {"email": customer_email},
            {"$set": {"subscription_status": 'active'}},
            return_document=ReturnDocument.AFTER
        )
    except Exception as e:
        print(f"Error handling subscription reactivated event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription reactivated event: {e}")