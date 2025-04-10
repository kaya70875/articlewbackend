from pydantic import BaseModel
from typing import List

class ParaphraseResponse(BaseModel):
    paraphrase: List[str]

class AIBasicResponse(BaseModel):
    response: str

class AIFeedbackResponse(BaseModel):
    check : str
    analysis : str

class CompareResponse(BaseModel):
    similarities: str
    differences: str
    examples_word1: List[str]
    examples_word2: List[str]

class FixGrammarResponse(BaseModel):
    original_sentence: str
    corrected_sentence: str
    raw_sentence: str