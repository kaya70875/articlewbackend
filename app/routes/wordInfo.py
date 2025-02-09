from fastapi import APIRouter
from app.models.word_info import WordInfoResponse
from word.wordNet import get_word_info_extended
from word.spacyWord import get_word_pos
import asyncio

router = APIRouter()

@router.get("/wordInfo/{word}" , response_model=WordInfoResponse)
async def get_word_info(word: str):
    try:
        # Call the function to get word information
        word_info = await asyncio.to_thread(get_word_info_extended, word)
        return word_info
    except LookupError:
        return 'NLTK data not found'
    except:
        return 'Something went wrong while getting word info'

@router.get("/wordPos/{word}/{sentence}")
async def get_word_Pos(word: str, sentence: str):
    # Call the function to get word information
    word_info = await asyncio.to_thread(get_word_pos, word, sentence)
    return {"response" : word_info}