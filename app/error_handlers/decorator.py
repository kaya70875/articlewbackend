from functools import wraps
from fastapi import HTTPException
import logging
from httpx import HTTPError, ReadTimeout

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPError:
            logging.exception('HTTPError occurred')
            raise HTTPException(status_code=502, detail='Error fetching data from AI')
        except ReadTimeout:
            logging.exception('Request timed out.')
            raise HTTPException(status_code=504, detail='Request timed out')
        except Exception as e:
            logging.exception(f'Error in {func.__name__}: {e}')
            raise HTTPException(status_code=500, detail='Internal Server Error')
    return wrapper