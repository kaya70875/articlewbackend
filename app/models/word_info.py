from pydantic import BaseModel, Field
from typing import List

class WordInfo(BaseModel):
    definition: str
    synonyms: List[str]
    examples: List[str]
class WordInfoResponse(BaseModel):
    adjective: List[WordInfo]
    adverb: List[WordInfo]
    verb: List[WordInfo]
    noun: List[WordInfo]
    pos : str

class WordSimilarityResponse(BaseModel):
    score: float

class WordSimilarityRequest(BaseModel):
    word1: str = Field(..., min_length=1, max_length=12, strip_whitespace=True)
    word2: str = Field(..., min_length=1, max_length=12, strip_whitespace=True)