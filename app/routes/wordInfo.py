from fastapi import APIRouter, HTTPException, Depends, Path
from app.models.word_info import *
from word.wordNet import get_word_info_extended
import asyncio
import logging
from word.spacyWord import calculate_similarity_score

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/wordInfo/{word}" , response_model=WordInfoResponse, response_description="Get word info like definition, synonyms, examples")
async def get_word_info(word: str = Path(description="The word to get info about", min_length=1, max_length=30, strip_whitespace=True)):
    try:
        # Call the function to get word information
        word_info = await asyncio.to_thread(get_word_info_extended, word)
        if word_info['pos'] is None:
            logger.error(f"Word not found! : {word}")
            raise HTTPException(status_code=404, detail="Word not found.")
        return word_info
    except LookupError:
        logger.error(f"NLTK data not found!")
        raise HTTPException(status_code=404, detail="NTLK Data not found.")
    except Exception as e:
        logger.error(f"Unexpected error occurred! : {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get('/wordSimilarity/{word1}/{word2}', response_model=WordSimilarityResponse, response_description="Get a similarity score between two words")
async def get_word_similarity(inputs : WordSimilarityRequest = Depends()):
    #Validete inputs
    if inputs.word1 == inputs.word2:
        logger.error('Got the same word as an input.')
        raise HTTPException(status_code=400, detail="Both words must not be the same.")

    # Call the function to get word information
    score = await asyncio.to_thread(calculate_similarity_score, inputs.word1, inputs.word2)

    return {"score" : round((score * 100), 2)}