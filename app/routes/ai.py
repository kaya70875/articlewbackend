from fastapi import APIRouter , HTTPException, Path
from typing import Literal
from app.models.aiResponse import *
from word.word_assistant import WordAssistant
from app.responses.validate import validate_json_response
from dotenv import load_dotenv
import os
from urllib.parse import unquote
import json
import logging
from typing import Annotated
from fastapi import Depends
from app.user.extract_jwt_token import get_user_id
from app.lib.request import track_requests

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')
word_assistant = WordAssistant(api_key)

router = APIRouter()

@router.get("/generate/{word}", response_model=AIFeedbackResponse, response_description="Check if word is valid and generate a response about how this word is used in a sentence.")
async def generate_response(user_id : Annotated[str, Depends(get_user_id)], word: str = Path(description="The word to generate a response about", min_length=1, max_length=30)):
    #Check for request limit.
    track_requests(user_id, 'generateReq')
    results = await word_assistant.analyze_word(word)

    if not results: 
        logger.warning('Response from AI is not a string or it is empty')
        raise HTTPException(status_code=404, detail="No results found.")
    
    return validate_json_response(AIFeedbackResponse, results)
    

@router.get("/analysis/{sentence}/{word}", response_model=AIBasicResponse, response_description="Analyze a sentence and generate a response about its grammar structure.")
async def analyze_sentence(
    user_id : Annotated[str, Depends(get_user_id)],
    sentence: str = Path(description="The sentence to analyze", min_length=1, max_length=400),
    word: str = Path(description="The word to analyze", min_length=1, max_length=30),):

    #Check for request limit.
    track_requests(user_id, 'grammarReq')

    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await word_assistant.analyze_sentence_with_word(sentence, word)
    
    return {"response": results}

@router.get("/grammar/{sentence}", response_model=FixGrammarResponse, response_description="Fix all grammar errors in a sentence. Additionally fixing spelling errors or typos.")
async def fix_grammar(user_id : Annotated[str, Depends(get_user_id)], sentence : str = Path(description="The sentence to fix", min_length=1, max_length=500)):

    #Check for request limit.
    track_requests(user_id, 'fixSentenceReq')

    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await word_assistant.fix_grammar_errors(sentence)
    return {"original_sentence": results[0], "corrected_sentence": results[1], "raw_sentence": results[2]}
    
@router.get("/paraphrase/{sentence}/{context}" , response_model=ParaphraseResponse, response_description="Generate a paraphrase of a sentence.")
async def generate_paraphrase(
    user_id : Annotated[str, Depends(get_user_id)],
    sentence : str = Path(description="The sentence to paraphrase", min_length=1, max_length=200),
    context: Literal['Casual', 'Formal', 'Sortened', 'Extended', 'Academic'] = Path(description="Context for the paraphrase", min_length=1, max_length=20),
    ):
    
    #Check for request limit.
    track_requests(user_id, 'paraphraseReq')

    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await word_assistant.paraphrase(sentence, context=context)
    return {"paraphrase": results}

@router.get("/compare/{word1}/{word2}", response_model=CompareResponse, response_description="Compare two words and generate a response about their similarities and differences.")
async def compare(
    user_id : Annotated[str, Depends(get_user_id)],
    word1: str = Path(description="The first word to compare", min_length=1, max_length=30),
    word2: str = Path(description="The second word to compare", min_length=1, max_length=30),
    ):

    #Check for request limit.
    track_requests(user_id, 'compareWordsReq')

    results = await word_assistant.compare_words(word1, word2)

    if not results:
        logger.warning('Response from AI is not a string or it is empty')
        raise HTTPException(status_code=404, detail='No results found')

    try:
        return validate_json_response(CompareResponse, results)
    except json.JSONDecodeError:
        logger.error('Invalid JSON response from AI')
        raise HTTPException(status_code=400, detail='Invalid JSON response from API')
        