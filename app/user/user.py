from app.models.database import db
from bson import ObjectId
from pymongo.errors import WriteError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import logging

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

def check_request_limit(user_info : dict, request_type : str, increment: int = 1) -> bool:

    """
    Checks request limits for a specific user based on current plan.
    """
    user_tier = user_info.get('user_tier')
    user_id = user_info.get('user_id')
    uid = ObjectId(user_id)
    now = datetime.now(timezone.utc)

    try:
        limits = USER_LIMITS.get(user_tier, USER_LIMITS["free"])
        limit = limits[request_type]

        now = datetime.now(timezone.utc)
        reset_date = now + timedelta(days=1)

        metrics_collection.update_one(
            {"_id": uid},
            {
                "$setOnInsert": {
                    "sentenceReq": 0,
                    "generateReq": 0,
                    "grammarReq": 0,
                    "paraphraseReq": 0,
                    "fixSentenceReq": 0,
                    "compareWordsReq": 0,
                    "reset_date": reset_date
                }
            },
            upsert=True
        )

        metrics_collection.update_one(
            {
                "_id": uid,
                "reset_date": {"$lte": now}
            },
            {
                "$set": {
                    "sentenceReq": 0,
                    "generateReq": 0,
                    "grammarReq": 0,
                    "paraphraseReq": 0,
                    "fixSentenceReq": 0,
                    "compareWordsReq": 0,
                    "reset_date": reset_date
                }
            }
        )

        result = metrics_collection.update_one(
            {
                "_id": uid,
                f"{request_type}": {"$lt": limit}
            },
            {
                "$inc": {request_type: increment}
            }
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=402,
                detail=f"Request limit exceeded for {request_type}"
            )

    except WriteError as write_err:
        logger.error(f'Error while writing the database {write_err}')
        raise WriteError(f'Error while writing the database {write_err}')
    except ValueError as v_err:
        logger.error(f'Error while getting current plan or request type {v_err}')
        raise HTTPException(status_code=400, detail=f'Error while getting current plan or request type {v_err}')
    except AttributeError as attr_err:
        logger.error(f'Error while accessing attr in reqeust limit ${attr_err}')
        raise HTTPException(status_code=400, detail=f'Error while accessing attr in request limit ${attr_err}')


