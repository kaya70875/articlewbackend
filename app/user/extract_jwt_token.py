from fastapi.security import HTTPBearer
from fastapi import Depends, Header
from typing import Annotated
from app.user.utils.helpers import *
from typing import Literal

security = HTTPBearer(
    description="Enter your JWT token from Next Auth"
)

async def get_user_id(credentials: Annotated[str, Depends(security)], provider : Literal['google', 'credentials'] = Header(None, alias='X-Provider')):
    # Get token from credentials
    token = credentials.credentials

    if provider == 'credentials':
        user_id = await extract_id_from_jwt(token)
        return user_id
    else:
        user_id = await extract_id_from_email(token)
        return user_id
