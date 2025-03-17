import logging
from app.models.database import db

logger = logging.getLogger(__name__)

async def extract_id_from_email(email : str):
    try:
        currentUser = db['users'].find_one({'email' : email})
        user_id = currentUser.get('_id')

        return user_id
    
    except Exception as e:
        logging.error('Exception happened', e)