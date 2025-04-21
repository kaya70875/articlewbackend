from app.models.database import db
from fastapi import HTTPException
from pymongo import ReturnDocument
from app.routes.paddle.utils import *
from app.routes.paddle.operations import *
import logging

logger = logging.getLogger(__name__)

def handleSubscriptionCreated(data: dict):
    """
    Handle the subscription created event from Paddle.
    This function should be called when a subscription is created.

    It should update the user's subscription status in the database.
    """

    try:
        # Get relevant fields
        sub_id = data.get("id")
        package_name = data.get("items")[0]["price"]["name"]

        # Get the customer email from Paddle
        customer_email = get_customer_email(data)

        users_collection = db.get_collection('users')
        res = users_collection.find_one_and_update(
            {"email": customer_email},
            {"$set": {"subscription_status": 'active',
                    "userType": package_name,
                    "subscription_id": sub_id,
                    }},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        logger.info(f"Subscription created for {customer_email}: {res}")
    except Exception as e:
        print(f"Error handling subscription created event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription created event: {e}")

def handleSubscriptionUpdated(data: dict):
    """
    Handle the subscription updated event from Paddle.
    This function should be called when a subscription is updated.

    It should update the user's subscription status in the database.
    """

    try:
        # Get action type
        action_type = data.get("scheduled_change")["action"] if data.get("scheduled_change") else None
        
        if action_type == 'cancel':
            # Handle cancel action
            res = cancel_subscription(data)
            logger.info(f"Subscription status updated to cancelled: {res}")
        else:
            # Activate the subscription status again
            res = reactivate_subscription(data)
            logger.info(f"Subscription status updated to active: {res}")
            
    except Exception as e:
        print(f"Error handling subscription updated event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription updated event: {e}")

def handleSubscriptionCanceled(data: dict):
    """
    Handle the subscription cancelled event from Paddle.
    This function should be called when a subscription is cancelled.

    It should update the user's subscription status in the database.
    """
    try:
        customer_email = get_customer_email(data)
        users_collection = db.get_collection('users')

        res = users_collection.find_one_and_update(
            {"email": customer_email},
            {"$set": {"subscription_status": 'inactive',
                    "userType": "Free",
                    "subscription_id": '',
                    }},
        )

        logger.info(f"Subscription cancelled for {customer_email}: {res}")
        
    except Exception as e:
        print(f"Error handling subscription cancelled event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription cancelled event: {e}")


