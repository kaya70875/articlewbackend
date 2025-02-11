import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import pytest
from fastapi import HTTPException
from httpx import HTTPError
from error_handlers.decorator import handle_exceptions

@pytest.mark.asyncio
async def test_handle_httperror():
    # Define a dummy async function that always raises an HTTPError.
    @handle_exceptions
    async def dummy_function():
        raise HTTPError("Test HTTPError")

    @handle_exceptions
    async def test_internal_server_error():
        raise HTTPException(status_code=500)

    # Use pytest.raises to ensure that calling dummy_function raises an HTTPException.
    with pytest.raises(HTTPException) as exc_info:
        await dummy_function()
    
    with pytest.raises(HTTPException) as int_info:
        await test_internal_server_error()

    # Check that the raised HTTPException has status code 502.
    assert exc_info.value.status_code == 502
    assert int_info.value.status_code == 500
