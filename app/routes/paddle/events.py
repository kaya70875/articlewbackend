from app.models.database import db
from fastapi import HTTPException
from pymongo import ReturnDocument
from app.routes.paddle.utils import *

async def handleSubscriptionCreated(data: dict):
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
        await users_collection.find_one_and_update(
            {"email": customer_email},
            {"$set": {"subscription_status": 'active',
                    "userType": package_name,
                    "subscription_id": sub_id,
                    }},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
    except Exception as e:
        print(f"Error handling subscription created event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription created event: {e}")
    
async def handleSubscriptionCanceled(data: dict):
    """
    Handle the subscription cancelled event from Paddle.
    This function should be called when a subscription is cancelled.

    It should update the user's subscription status in the database.
    """
    try:
        customer_email = get_customer_email(data)
        users_collection = db.get_collection('users')

        await users_collection.find_one_and_update(
            {"email": customer_email},
            {"$set": {"subscription_status": 'inactive',
                    "userType": "Free",
                    "subscription_id": '',
                    }},
        )
        
    except Exception as e:
        print(f"Error handling subscription cancelled event: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling subscription cancelled event: {e}")


