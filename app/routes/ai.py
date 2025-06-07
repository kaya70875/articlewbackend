from fastapi import APIRouter , HTTPException, Path
from typing import Literal
from app.models.aiResponse import *
from word.deepseek import *
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
from app.lib.rd import r
import time

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')

router = APIRouter()

@router.get("/generate/{word}", response_model=AIFeedbackResponse, response_description="Check if word is valid and generate a response about how this word is used in a sentence.")
async def generate_response(user_id : Annotated[str, Depends(get_user_id)], word: str = Path(description="The word to generate a response about", min_length=1, max_length=30)):
    start = time.perf_counter()
    #Check for request limit.

    track_requests(user_id, 'generateReq')

    results = await analyze_word(word, api_key)
        
    if isinstance(results, str):
        parsed_results = json.loads(results.strip("```json").strip("```").strip())
        end = time.perf_counter()
        print(f'Took {end - start} seconds to generate AI response.')
        return validate_json_response(AIFeedbackResponse, parsed_results)

    else:
        logger.warning('Response from AI is not a string or it is empty')
        raise HTTPException(status_code=404, detail="No results found.")

@router.get("/analysis/{sentence}/{word}", response_model=AIBasicResponse, response_description="Analyze a sentence and generate a response about its grammar structure.")
async def analyze_sentence(
    user_id : Annotated[str, Depends(get_user_id)],
    sentence: str = Path(description="The sentence to analyze", min_length=1, max_length=400),
    word: str = Path(description="The word to analyze", min_length=1, max_length=30),):

    #Check for request limit.
    track_requests(user_id, 'grammarReq')

    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await analyze_sentence_with_word(sentence, word, api_key)
    
    return {"response": results}

@router.get("/grammar/{sentence}", response_model=FixGrammarResponse, response_description="Fix all grammar errors in a sentence. Additionally fixing spelling errors or typos.")
async def fix_grammar(user_id : Annotated[str, Depends(get_user_id)], sentence : str = Path(description="The sentence to fix", min_length=1, max_length=500)):

    #Check for request limit.
    track_requests(user_id, 'fixSentenceReq')

    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await fix_grammar_errors(sentence, api_key)
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
    results = await paraphrase(sentence, api_key, context=context)
    return {"paraphrase": results}

@router.get("/compare/{word1}/{word2}", response_model=CompareResponse, response_description="Compare two words and generate a response about their similarities and differences.")
async def compare(
    user_id : Annotated[str, Depends(get_user_id)],
    word1: str = Path(description="The first word to compare", min_length=1, max_length=30),
    word2: str = Path(description="The second word to compare", min_length=1, max_length=30),
    ):

    #Check for request limit.
    track_requests(user_id, 'compareWordsReq')

    results = await compare_words(word1, word2, api_key)

    if results:
        try:
            parsed_results = json.loads(results.strip("```json").strip("```").strip())
            return validate_json_response(CompareResponse, parsed_results)
        except json.JSONDecodeError:
            logger.error('Invalid JSON response from AI')
            raise HTTPException(status_code=400, detail='Invalid JSON response from API')
        
    else:
        logger.warning('Response from AI is not a string or it is empty')
        raise HTTPException(status_code=404, detail='No results found')