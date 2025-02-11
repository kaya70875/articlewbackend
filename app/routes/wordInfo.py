from fastapi import APIRouter
from app.models.word_info import *
from word.wordNet import get_word_info_extended
from word.spacyWord import get_word_pos
import asyncio
from word.spacyWord import calculate_similarity_score

router = APIRouter()

@router.get("/wordInfo/{word}" , response_model=WordInfoResponse, response_description="Get word info like definition, synonyms, examples")
async def get_word_info(word: str):
    try:
        # Call the function to get word information
        word_info = await asyncio.to_thread(get_word_info_extended, word)
        return word_info
    except LookupError:
        return 'NLTK data not found'
    except:
        return 'Something went wrong while getting word info'

@router.get('/wordSimilarity/{word1}/{word2}', response_model=WordSimilarityResponse, response_description="Get a similarity score between two words")
async def get_word_similarity(word1: str, word2: str):
    # Call the function to get word information
    score = await asyncio.to_thread(calculate_similarity_score, word1, word2)
    percentage = (score * 100)
    return {"score" : percentage.__round__(2)}