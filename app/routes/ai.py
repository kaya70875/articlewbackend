from fastapi import APIRouter , HTTPException
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.models.paraphraseModel import ParaphraseModel as pModel
from word.deepseek import analyze_word , analyze_sentence_with_word, fix_grammar_errors, paraphrase, compare_words
from dotenv import load_dotenv
import os
from urllib.parse import unquote

load_dotenv()
api_key = os.getenv('HUGGING_FACE_API_KEY')


router = APIRouter()

#Choose a device (cpu or cuda)
device = "cuda" if torch.cuda.is_available() else "cpu"

#Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")
model = AutoModelForSeq2SeqLM.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base").to(device)

@router.get("/generate/{word}")
async def generate_response(word: str):
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    try:
        results = await analyze_word(word, api_key)
        return {"response": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{sentence}/{word}")
async def analyze_sentence(sentence: str, word: str):
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    try:
        sentence = unquote(sentence) # filter out special characters from url like ? , . etc
        results = await analyze_sentence_with_word(sentence, word, api_key)
        return {"response": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/grammar/{sentence}")
async def fix_grammar(sentence : str):
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    try:
        sentence = unquote(sentence) # filter out special characters from url like ? , . etc
        results = await fix_grammar_errors(sentence, api_key)
        return {"response": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/paraphrase/{sentence}/{context}" , response_model=pModel)
async def generate_paraphrase(sentence : str, context: str):
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    try:
        sentence = unquote(sentence) # filter out special characters from url like ? , . etc
        results = await paraphrase(sentence, api_key, context=context)
        return {"paraphrase": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compare/{word1}/{word2}")
async def compare(word1: str, word2: str):
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    try:
        results = await compare_words(word1, word2, api_key)
        return {"response": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))