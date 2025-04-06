import os
import jwt
from fastapi import HTTPException
from app.models.database import db
from json import JSONDecodeError
import logging
import httpx

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
    except jwt.PyJWTError as py_err:
        logger.error(f'Invalid authentication credentials. Details: ${py_err}')
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def extract_id_from_email(token: str):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )

        if res.status_code != 200:
            logger.error(f"Error fetching user info: {res.status_code} - {res.text}")
            raise HTTPException(status_code=res.status_code, detail="Failed to fetch user info")

        response = res.json()
        email = response['email']

        currentUser = db['users'].find_one({'email': email})
        user_id = currentUser.get('_id')

        return user_id
    except httpx.HTTPStatusError as http_err:
        logger.error(f'HTTP error: {http_err}')
        raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
    except JSONDecodeError as json_err:
        logger.error(f'Invalid json structure from request object: {json_err}')
        raise HTTPException(status_code=400, detail=f'Invalid json structure from request object: {json_err}')
    except ValueError as v_err:
        logger.error(f'Value error: {v_err}')
        raise HTTPException(status_code=400, detail=f'Value error: {v_err}')

