import time
import json
import httpx
import logging
from typing import Optional
from fastapi import HTTPException

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_chat_completion(api_key: str, content: dict, temperature: int = 1.3, response_format: str = 'text'):
    """
    Get a chat completion response from the DeepSeek AI model.

    Args:
        api_key (str): The API key for authentication with the DeepSeek API.
        messages (list[dict]): A list of message dictionaries containing the conversation history.

    Returns:
        str: The content of the AI's response to the provided messages.
    """

    
    from openai import OpenAI

    try:
        start = time.perf_counter()
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role" : "system",
                    "content" : "You are a helpful assistant."
                },
                content
            ],
            temperature=temperature,
            response_format={'type' : response_format},
            stream=False
        )

        if not response:
            raise HTTPException(status_code=500, detail='Response from AI is not valid.')
        end = time.perf_counter()
        print(f'Took {end - start} seconds to return AI message.')

        ai_resp = response.choices[0].message.content
        return json.loads(ai_resp) if response_format == 'json_object' else ai_resp
    except Exception as e:
        logger.error(f'Error while getting chat completion {e}')
        raise HTTPException(status_code=500, detail=f'Error while getting chat completion {e}')

async def make_httpx_request(api_key : str, messages: list[dict], parameters : Optional[dict] = None) -> str:

    """Make a request to the Hugging Face inference API.

    Args:
        api_key (str): The API key for authentication
        messages (list[dict]): List of message dictionaries like user , content
        parameters (Optional): Request parameters like temperature and max_new_tokens

    Returns:
        str: Generated text response
    """

    default_parameters = {
        "temperature" : 0.2,
    }

    request_parameters = {**default_parameters, **(parameters or {})}

    if not messages[0]["content"]:
        logger.error("No messages found in the AI response")
        raise ValueError("No messages found in the response")


    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "inputs": messages[0]["content"],
                "parameters": request_parameters
            },
            timeout=30.0 #Increased timeout
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        completion = response.json()

        # Prepare the request payload
        if not completion:
            logger.error("Invalid response from the API")
            raise ValueError("Invalid response from the API")
        
        response_text = completion[0]["generated_text"]
        return response_text