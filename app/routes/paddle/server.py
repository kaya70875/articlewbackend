from paddle_billing import Client, Environment, Options
from typing import List
from os import getenv
from fastapi import APIRouter, HTTPException, Request
from app.utils.signature import verify_paddle_signature
from app.routes.paddle.events import *
from app.models.paddle import *

if not getenv("PADDLE_API_SECRET"):
    raise ValueError("PADDLE_API_SECRET is not set in the environment.")

paddle = Client(getenv('PADDLE_API_SECRET'), options=Options(Environment.SANDBOX))

router = APIRouter()

@router.get("/paddle/prices", response_model=List[PaddlePrice])
async def get_prices():
    """
    Get the prices from Paddle.
    """
    try:
        paddle_prices = paddle.prices.list()

        #Create a free tier for free users
        free_tier = {
            "name" : "Free",
            "description" : "Basic plan for free users",
            "price_id" : "",
            "amount" : '0',
            "currency": "USD",
            "product_id" : "",
            "limits": {
                "search" : "50 / day",
                "generate" : "10 / day",
                "grammar" : "7 / day",
                "paraphrase" : "7 / day",
                "fix" : "7 / day",
                "compare": "7 / day",
            }
        }

        all_prices = [
            {
                "name" : price.name,
                "description" : price.description,
                "price_id": price.id,
                "amount": price.unit_price.amount,
                "currency": price.unit_price.currency_code.value,
                "product_id": price.product_id,
                "limits": price.custom_data.data if price.custom_data else {}
            }
            for price in paddle_prices
            
        ]

        # Add the free tier to the list of prices
        all_prices.insert(0, free_tier)

        return all_prices
    except Exception as e:
        print(f"Error retrieving prices: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving prices: {e}")

@router.get("/paddle/subscriptions/{subscription_id}", response_model=PaddleSubscription)
async def get_subscription(subscription_id: str):
    """
    Get the subscription details from Paddle.
    """
    try:
        subscription = paddle.subscriptions.get(subscription_id)

        return {
            "subscription_id": subscription.id,
            "next_billed_at": subscription.next_billed_at,
            "cancellation_effective_at": subscription.scheduled_change.effective_at if subscription.scheduled_change else None,
            "update_url": subscription.management_urls.update_payment_method,
            "cancel_url" : subscription.management_urls.cancel
        }
    except Exception as e:
        print(f"Error retrieving subscription: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving subscription: {e}")

@router.post("/webhook")
async def webhook(req: Request):
    try:
        # Verify the signature
        body = await req.body()

        if not verify_paddle_signature(req.headers, body):
            raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Parse the JSON body
        json_data = await req.json()
        data = json_data.get("data")
        
        # Check if the event type is present
        event_type = json_data.get("event_type")
        if not event_type:
            return HTTPException(status_code=400, detail="Missing event_type in request body")
        
        # Handle different event types
        if event_type == "subscription.created":
            # Handle subscription created event
            handleSubscriptionCreated(data)
        
        elif event_type == "subscription.updated":
            # Handle subscription updated event
            print(data)
            handleSubscriptionUpdated(data)
        
        elif event_type == "subscription.cancelled":
            # Handle subscription cancelled event
            handleSubscriptionCanceled(data)
    
        else:
            print(f"Unhandled event type: {event_type}")
        
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"❌ Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Error handling webhook: {e}")
