from pydantic import BaseModel
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