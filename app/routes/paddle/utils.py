from fastapi import HTTPException

def get_customer_email(data: dict) -> str:
    """
    Extract the customer email from the request data.
    This function is used to handle Paddle webhook events.
    """
    customer_email = data.get("custom_data")["email"]
    if not customer_email:
        raise HTTPException(status_code=400, detail="Missing customer email in request data")
    
    return customer_email