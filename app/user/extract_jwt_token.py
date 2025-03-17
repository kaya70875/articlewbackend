from app.user.utils.helpers import *
from fastapi_nextauth_jwt import NextAuthJWTv4
from typing import Annotated
from fastapi import Depends, HTTPException
import os

SECRET_KEY = os.getenv('JWT_SECRET')
JWT = NextAuthJWTv4(secret=SECRET_KEY)

async def get_user_id(jwt : Annotated[dict, Depends(JWT)]):
    """
    Gets user's details with decoding jwt token.
    """

    provider = jwt['provider']
    
    if provider == 'credentials':
        user_id = jwt.get('id')
        if not user_id:
            raise HTTPException(status_code=401, detail='User id cannot found in token.')
        return user_id
    else:
        email = jwt.get('email')
        user_id = await extract_id_from_email(email)
        return user_id