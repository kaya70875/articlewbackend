import jwt
from fastapi import HTTPException
from json import JSONDecodeError
import logging
from app.models.database import db
import os

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv('JWT_SECRET')
ALGORITHM = 'HS256'

async def extract_id_from_jwt(token : str):
    try:        
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail='Could not extract user ID from token',
                headers={"WWW-Authenticate": "Bearer"},
            )
                
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def extract_id_from_email(token : str):
    import requests

    try:
        res = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {token}"}
        )

        response = res.json()
        email = response['email']

        currentUser = db['users'].find_one({'email' : email})
        user_id = currentUser.get('_id')

        return user_id
    
    except JSONDecodeError as json_err:
        logger.error(f'Invalid json structure from request object ${json_err}')
        raise HTTPException(status_code=400, detail=f'Invalid json structure from request object ${json_err}')
    except ValueError as v_err:
        logger.error(f'Value error ${v_err}')
        raise HTTPException(status_code=400, detail=f'Value error ${v_err}')