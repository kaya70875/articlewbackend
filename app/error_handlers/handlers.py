import logging
import httpx
import logging
import json
from fastapi.responses import JSONResponse
from fastapi import Request
from httpx import ReadTimeout

logger = logging.getLogger(__name__)

exception_handlers = {}

def register_exception_handler(exc_class):
    """
    Decorator to register exception handlers
    """
    def decorator(func):
        exception_handlers[exc_class] = func
        return func
    return decorator

@register_exception_handler(httpx.HTTPError)
async def http_exception_handler(request : Request, exc:httpx.HTTPError):
    logger.error(f'HTTP error occured {exc}')
    return JSONResponse(
        status_code=500,
        content={'detail' : f'Http error occured {exc}'}
    )
@register_exception_handler(json.JSONDecodeError)
async def json_decode_error_handler(request : Request, exc:json.JSONDecodeError):
    logger.error(f'Invalid json data {exc}')
    return JSONResponse(
        status_code=400,
        content={'detail' : f'Invalid json data {exc}'}
    )
@register_exception_handler(KeyError)
async def key_error_handler(request : Request, exc:KeyError):
    logger.error(f'Invalid key {exc}')
    return JSONResponse(
        status_code=400,
        content = {'detail' : f'Invalid key {exc}'}
    )
@register_exception_handler(ReadTimeout)
async def timeout_error_handler(request : Request, exc: ReadTimeout):
    logger.error(f'Request timed out {exc}')
    return JSONResponse(
        status_code=408,
        content={'detail' : f'Request timed out {exc}'}
    )

def setup_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app
    """
    for exc_class, handler in exception_handlers.items():
        app.add_exception_handler(exc_class, handler)