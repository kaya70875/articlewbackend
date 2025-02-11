from fastapi import APIRouter , HTTPException
from app.models.aiResponse import *
from word.deepseek import *
from dotenv import load_dotenv
import os
from urllib.parse import unquote
import json
from app.error_handlers.decorator import handle_exceptions
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv('HUGGING_FACE_API_KEY')

router = APIRouter()

@router.get("/generate/{word}", response_model=AIFeedbackResponse, response_description="Check if word is valid and generate a response about how this word is used in a sentence.")
@handle_exceptions
async def generate_response(word: str):
    results = await analyze_word(word, api_key)
        
    if isinstance(results, str):
        try:
            parsed_results = json.loads(results.strip("```json").strip("```").strip())
            return parsed_results
        except json.JSONDecodeError:
            logging.error("Invalid JSON response from AI")
            raise HTTPException(status_code=500, detail="Invalid JSON response from AI")
        
    else:
        logger.warning('Response from AI is not a string or it is empty')
        raise HTTPException(status_code=404, detail="No results found.")

@router.get("/analysis/{sentence}/{word}", response_model=AIBasicResponse, response_description="Analyze a sentence and generate a response about its grammar structure.")
@handle_exceptions
async def analyze_sentence(sentence: str, word: str):
    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await analyze_sentence_with_word(sentence, word, api_key)
    return {"response": results}

@router.get("/grammar/{sentence}", response_model=FixGrammarResponse, response_description="Fix all grammar errors in a sentence. Additionally fixing spelling errors or typos.")
@handle_exceptions
async def fix_grammar(sentence : str):
    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await fix_grammar_errors(sentence, api_key)
    return {"original_sentence": results[0], "corrected_sentence": results[1]}
    


@router.get("/paraphrase/{sentence}/{context}" , response_model=ParaphraseResponse, response_description="Generate a paraphrase of a sentence.")
@handle_exceptions
async def generate_paraphrase(sentence : str, context: str):
    sentence = unquote(sentence) # filter out special characters from url like ? , . etc
    results = await paraphrase(sentence, api_key, context=context)
    return {"paraphrase": results}

@router.get("/compare/{word1}/{word2}", response_model=CompareResponse, response_description="Compare two words and generate a response about their similarities and differences.")
@handle_exceptions
async def compare(word1: str, word2: str):
    results = await compare_words(word1, word2, api_key)

    if results:
        try:
            parsed_results = json.loads(results.strip("```json").strip("```").strip())
            return parsed_results # ✅ Return structured JSON directly
        except json.JSONDecodeError:
            logger.error('Invalid JSON response from AI')
            raise HTTPException(status_code=500, detail='Invalid JSON response from API')
        
    else:
        logger.warning('Response from AI is not a string or it is empty')
        raise HTTPException(status_code=404, detail='No results found')