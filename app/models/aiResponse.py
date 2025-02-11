from pydantic import BaseModel
from typing import List

class ParaphraseModel(BaseModel):
    paraphrase: List[str]

class AIResults(BaseModel):
    response: str

class AIFeedbackResponse(BaseModel):
    check : str
    analysis : str

class CompareResults(BaseModel):
    similarities: str
    differences: str
    examples_word1: List[str]
    examples_word2: List[str]