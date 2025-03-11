from fastapi.security import HTTPBearer
from fastapi import Depends, Header
from typing import Annotated
from typing import Literal
from app.user.utils.helpers import *

security = HTTPBearer(
    description="Enter your JWT token from Next Auth"
)

async def get_user_id(credentials: Annotated[str, Depends(security)], provider : Literal['google', 'credentials'] = Header(None, alias='X-Provider')):
    """
    Gets user's details with decoding jwt token.
    """
    # Get token from credentials
    token = credentials.credentials
        
    if provider == 'credentials':
        print('credentials!!!')
        user_id = await extract_id_from_jwt(token)
        return user_id
    else:
        user_id = await extract_id_from_email(token)
        return user_id