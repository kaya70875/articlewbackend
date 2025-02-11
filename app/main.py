from fastapi import FastAPI
from app.routes.sentences import router as sentences_route
from app.routes.ai import router as ai_route
from fastapi.middleware.cors import CORSMiddleware
from app.routes.wordInfo import router as wordInfo_route
import nltk
import os
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your routes
app.include_router(sentences_route, prefix="/api", tags=["Sentences"])
app.include_router(ai_route, prefix="/api", tags=["AI"])
app.include_router(wordInfo_route, prefix="/api", tags=["WordInfo"])

async def validate_env():
    if not os.getenv("HUGGING_FACE_API_KEY"):
        import logging
        logging.error("HUGGING_FACE_API_KEY is not set in the environment.")
        sys.exit("Missing HUGGING_FACE_API_KEY")

nltk.data.path.append(os.getenv("NLTK_DATA", "./nltk_data"))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
