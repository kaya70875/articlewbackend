from os import getenv
import hmac
import hashlib
import time

def verify_paddle_signature(headers: dict, body: bytes) -> bool:

    """
    Verify the Paddle webhook signature.
    :param headers: The headers from the request.
    :param body: The body of the request.
    :return: True if the signature is valid, False otherwise.
    """

    paddle_signature = headers.get('Paddle-Signature')
    if not paddle_signature:
        return False

    webhook_secret = getenv('WEBHOOK_SECRET')
    if not webhook_secret:
        return False

    x = paddle_signature.split(';')

    ts = x[0].split('=')[1]
    h1 = x[1].split('=')[1]

    # Optional: guard against replay attacks (5s tolerance)
    if abs(time.time() - int(ts)) > 5:
        return False

    signed_payload = f"{ts}:{body.decode('utf-8', errors='ignore')}"

    computed_h1 = hmac.new(
    key=webhook_secret.encode('utf-8'),
    msg=signed_payload.encode('utf-8'),
    digestmod=hashlib.sha256
    ).hexdigest()

    return h1 == computed_h1