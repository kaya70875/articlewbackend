from app.models.database import db
from bson import ObjectId
from pymongo.errors import WriteError
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException

logger = logging.getLogger(__name__)

metrics_collection = db['userMetrics']

USER_LIMITS = {
    "basic": {
        "generateReq": 5,
        "paraphraseReq": 5,
        "fixSentenceReq": 5,
        "compareWordsReq": 5
    },
    "medium": {
        "generateReq": 10,
        "paraphraseReq": 10,
        "fixSentenceReq": 10,
        "compareWordsReq": 10
    },
    "premium": {
        "generateReq": 20,
        "paraphraseReq": 20,
        "fixSentenceReq": 20,
        "compareWordsReq": 20
    }
}

#TODO Reset usage limits after one day.

def get_user_tier(user_id : str) -> str:
    """
    Retrieve user type (basic, medium, premium) from the users collection.
    """
    try:
        user = db['users'].find_one({'_id' : ObjectId(user_id)})
        return user.get('userType')
    except AttributeError as attr_err:
        logger.error(f'Error while accessing attr ${attr_err}')
        raise HTTPException(status_code=400, detail=f'Error while accessing attr ${attr_err}')

def check_request_limit(user_id : str, request_type : str):

    """
    Checks request limits for a specific user based on current plan.
    """

    user_tier = get_user_tier(user_id).lower()

    try:
        metrics = metrics_collection.find_one({'_id' : ObjectId(user_id)})
        print('metrics', metrics)
        
        if not metrics:
            #If no record, create a new with reset time
            metrics_collection.insert_one({
                '_id' : ObjectId(user_id),
                'generateReq' : 0,
                'paraphraseReq' : 0,
                'fixSentenceReq' : 0,
                'compareWordsReq' : 0,
                'reset_date' : datetime.now() + timedelta(days=1) # Reset in one days
            })
            return

        #Check if user exceed the limit
        limits = USER_LIMITS.get(user_tier, USER_LIMITS['basic'])
        if metrics[request_type] >= limits[request_type]:
            logger.info('Request limit exceeded.')
            raise HTTPException(f'Request limit exceed. {request_type}')

        #Increase request count
        metrics_collection.update_one({'_id' : ObjectId(user_id) }, {"$inc" : {request_type : 1}})

    except WriteError as write_err:
        logger.error(f'Error while writing the database {write_err}')
        raise WriteError(f'Error while writing the database {write_err}')
    except ValueError as v_err:
        logger.error(f'Error while getting current plan or request type {v_err}')
        raise HTTPException(status_code=400, detail=f'Error while getting current plan or request type {v_err}')
    except AttributeError as attr_err:
        logger.error(f'Error while accessing attr ${attr_err}')
        raise HTTPException(status_code=400, detail=f'Error while accessing attr ${attr_err}')


