from app.lib.rd import r
from app.user.user import check_request_limit

# In this solution if users had reached their limit, check_request_limit function going to run every request which is not efficient.
# Instead we could track a key for checking request type if paymend required or not and not run check_request_limit function at all.
# We could just check the top and raise appropriate 402 message here.
def track_requests(user_id: str, request_type: str, request_count: int = 5):

    """
    Track requests to insert after number of requests for optimizing database operations.
    """
    key = f"user:{user_id}:requests"
    current_count = int(r.hget(key, request_type))

    if current_count % request_count == 0:
        is_payment_required = check_request_limit(user_id, request_type, request_count)
        if not is_payment_required:
            r.hincrby(key, request_type, 1)

    r.hincrby(key, request_type, 1)
    r.expire(key, 86400)  # 24 hours