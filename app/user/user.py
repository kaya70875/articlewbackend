from app.models.database import db
from bson import ObjectId
from pymongo.errors import WriteError
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException
from pymongo import ReturnDocument

logger = logging.getLogger(__name__)

metrics_collection = db['userMetrics']

UNLIMITED = 100000

USER_LIMITS = {
    "free": {
        "sentenceReq" : 50,
        "generateReq": 10,
        "grammarReq" : 7,
        "paraphraseReq": 7,
        "fixSentenceReq": 7,
        "compareWordsReq": 7
    },
    "premium": {
        "sentenceReq" : UNLIMITED,
        "generateReq": 100,
        "grammarReq" : 100,
        "paraphraseReq": 100,
        "fixSentenceReq": 100,
        "compareWordsReq": 100
    },
    "premium_plus": {
        "sentenceReq" : UNLIMITED,
        "generateReq": UNLIMITED,
        "grammarReq" : 500,
        "paraphraseReq": UNLIMITED,
        "fixSentenceReq": UNLIMITED,
        "compareWordsReq": 500
    }
}

def get_user_tier(user_id : str) -> str:
    """
    Retrieve user type (free, premium, premium_plus) from the users collection.
    """
    try:
        user = db['users'].find_one({'_id' : ObjectId(user_id)})
        return user.get('userType')
    except AttributeError as attr_err:
        logger.error(f'Error while accessing attr ${attr_err}')
        raise HTTPException(status_code=400, detail=f'Error while accessing attr ${attr_err}')

#TODO Consider handling all actions in one atomic way instead of if else block.

def check_request_limit(user_id : str, request_type : str):

    """
    Checks request limits for a specific user based on current plan.
    """

    user_tier = get_user_tier(user_id).lower().replace(' ', '_')
    now = datetime.now()

    try:
        metrics = metrics_collection.find_one({'_id' : ObjectId(user_id)})
        #print('metrics', metrics)
        
        if not metrics or metrics.get('reset_date', now) <= now:
            #If no record, create a new with reset time
            updated_metrics = metrics_collection.find_one_and_update(
                {"_id" : ObjectId(user_id)},
                {"$set" : {
                    'sentenceReq' : 0,
                    'generateReq' : 0,
                    'grammarReq' : 0,
                    'paraphraseReq' : 0,
                    'fixSentenceReq' : 0,
                    'compareWordsReq' : 0,
                    'reset_date' : now + timedelta(days=1) # Reset request limits after one day.
                }},
                upsert=True,
                return_document=ReturnDocument.AFTER
                )
        else : 
            updated_metrics = metrics
            
        #Check if user exceed the limit
        limits = USER_LIMITS.get(user_tier, USER_LIMITS['free'])

        if updated_metrics[request_type] >= limits[request_type]:
            logger.info('Request limit exceeded.')
            raise HTTPException(status_code=402, detail=f'Request limit exceed. {request_type}. Payment Required.')

        #Increase request count if user has request limit
        metrics_collection.update_one({'_id' : ObjectId(user_id) }, {"$inc" : {request_type : 1}})

    except WriteError as write_err:
        logger.error(f'Error while writing the database {write_err}')
        raise WriteError(f'Error while writing the database {write_err}')
    except ValueError as v_err:
        logger.error(f'Error while getting current plan or request type {v_err}')
        raise HTTPException(status_code=400, detail=f'Error while getting current plan or request type {v_err}')
    except AttributeError as attr_err:
        logger.error(f'Error while accessing attr in reqeust limit ${attr_err}')
        raise HTTPException(status_code=400, detail=f'Error while accessing attr in request limit ${attr_err}')


