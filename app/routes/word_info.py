from fastapi import APIRouter, HTTPException, Depends, Path
from app.models.word_info import *
from word.wordkit import Wordkit
import asyncio
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/wordInfo/{word}" , response_model=WordInfoResponse, response_description="Get word info like definition, synonyms, examples")
async def get_word_info(word: str = Path(description="The word to get info about", min_length=1, max_length=30, strip_whitespace=True)):
    try:
        wordkit = Wordkit(word)
        word_info = await asyncio.to_thread(wordkit.get_word_info_extended)
        if word_info.get('pos') is None:
            logger.error(f"Word not found! : {word}")
            raise HTTPException(status_code=404, detail="Word not found.")
        return word_info
    except LookupError:
        logger.error(f"NLTK data not found!")
        raise HTTPException(status_code=404, detail="NTLK Data not found.")
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error occurred! : {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")