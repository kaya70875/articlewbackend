from pydantic import BaseModel
from typing import List

class ParaphraseModel(BaseModel):
    paraphrase: List[str]