from app.lib.rd import r
from app.user.user import check_request_limit

def track_requests(user_id: str, request_type: str, request_count: int = 5):

    """
    Track requests to insert after number of requests for optimizing database operations.
    """

    key = f"user:{user_id}:requests"
    current_count = r.hincrby(key, request_type, 1)

    r.expire(key, 86400)  # 24 hours

    print(f'current count for {request_type} is :', current_count)

    if current_count % request_count == 0:
        check_request_limit(user_id, request_type, request_count)