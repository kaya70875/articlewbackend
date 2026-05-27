from fastapi import APIRouter, HTTPException, Query, Path, Depends
from app.models.database import sentences_collection
from app.utils.text_helpers import extract_sentences_from_raw_text
from pymongo.errors import CursorNotFound
from pymongo.cursor import Cursor
from typing import Annotated
from app.user.extract_jwt_token import get_user_info
from app.user.user import check_request_limit
import logging
import asyncio

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/sentences/{word}")
async def sentences(
    user_info : Annotated[dict, Depends(get_user_info)],
    word: str = Path(description="The word to search for in sentences", min_length=1, max_length=200),
    categories: str = Query(None, description="Comma-separated list of categories"),
    min_length: int = Query(None, description="Minimum sentence length"),
    max_length: int = Query(None, description="Maximum sentence length"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page"),
):
    """
    Get sentences containing the word, optionally filtered by categories, length, and sorted.
    """
    #await asyncio.to_thread(check_request_limit, user_info, 'sentenceReq')

    try:
        filter_query = {"$text": {"$search": word}}

        # Add categories to the filter if provided
        if categories:
            category_list = categories.split(',')
            filter_query['category'] = {'$in': category_list}
        
        if categories and not isinstance(categories, list):
            categories = [categories]

        # Add length filters if provided
        if min_length is not None or max_length is not None:
            filter_query['length'] = {}
            if min_length is not None:
                filter_query['length']['$gte'] = min_length
            if max_length is not None:
                filter_query['length']['$lte'] = max_length

        skip = (page - 1) * page_size

        total_results, results = await asyncio.gather(
            asyncio.to_thread(sentences_collection.count_documents, filter_query),
            asyncio.to_thread(get_cursors, filter_query, skip, page_size)
        )

        filtered_results = get_filtered_sentences(results, word)
        total_pages = -(-total_results // page_size)
        return {
            'word': word,
            'sentences': filtered_results,
            'total_results': total_results,
            'total_pages': total_pages,
            'categories': categories,
            'min_length': min_length,
            'max_length': max_length,
        }
    except CursorNotFound as cursor_err:
        logger.error(f'Cursor not found! {cursor_err}')
        raise HTTPException(status_code=400, detail=f'Curson not found! {cursor_err}')

def get_cursors(filter_query: dict, skip: int, page_size: int) -> list[Cursor]:
    cursor = sentences_collection.find(filter_query, {'_id': 0, 'text': 1, 'category': 1, 'source': 1}).skip(skip).limit(page_size)
    return list(cursor)


def get_filtered_sentences(results: list[Cursor], word: str) -> list[str]:
    filtered_results = extract_sentences_from_raw_text(results, word)

    # Handle no results
    if not results:
        logger.info("No sentences found for the given word and filters")
        raise HTTPException(status_code=404, detail="No sentences found for the given word and filters")

    return filtered_results
