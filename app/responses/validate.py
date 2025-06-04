from pydantic import BaseModel, ValidationError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def validate_json_response(model: type[BaseModel], data: dict):
    try:
        return model(**data)
    except ValidationError as e:
        logger.error(f'Invalid response format {e}')
        raise HTTPException(status_code=500, detail=f"Invalid response format {e}")