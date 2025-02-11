from utils.helpers import make_httpx_request, highlight_corrections, extract_paraphrase_sentences, parse_AI_response
import asyncio

async def analyze_word(word: str, api_key: str) -> str:
    """
    Analyze a word and provide an example of its usage in a sentence. 
    Additionally checks if word itself is correct or not in writing English.

    Args:
        word (str): The word to analyze.
        api_key (str): The API key for the Hugging Face model.
    Returns:
        str: The analysis of the word with an example sentence.
    """
    messages = [
        {
            "role": "user",
            "content": f"Can you analyze the word '{word}' and give an example of its usage? Additionally check if word itself is correct or not. Do not analysis word's origin and please keep it short. Give me a json Here an example json response: {{\"check\": \"'prevent' is a correct and usable word in written English.\",\"analysis\" : \"It can be used to describe a situation in which something bad is avoided from happening. For example: 'Taking precautions helped us prevent the spread of the virus.'\"}}"
        }
    ]

    response_text = await make_httpx_request(api_key, messages)
    final_answer = parse_AI_response(response_text, messages)

    return final_answer

async def analyze_sentence_with_word(sentence : str, word : str, api_key: str) -> str:
    """
    Analyze a sentence with a focus on a specific word and provide an explanation of its role, purpose, and meaning in the sentence.

    Args:
        sentence (str): The sentence to analyze.
        word (str): The word to focus on in the sentence.
        api_key (str): The API key for the Hugging Face model.
    Returns:
        str: The analysis of the sentence with a focus on the word.
    """
    messages = [
        {
            "role": "user",
            "content": f"Analyze the sentence: '{sentence}' with a focus on the word '{word}'. Explain its role, purpose, and meaning in the sentence in simple terms. Provide an example of a similar sentence using the word. Suggest an alternative way to rewrite the sentence with the same meaning. Keep the response clear and concise."
        }
    ]

    response_text = await make_httpx_request(api_key, messages)
    final_answer = parse_AI_response(response_text, messages)

    return final_answer

async def fix_grammar_errors(sentence : str, api_key : str) -> str:
    """
    Identify and fix any grammar errors in a sentence. If the sentence is already correct, return the original sentence.

    Args:
        sentence (str): The sentence to correct.
        api_key (str): The API key for the Hugging Face model.
    Returns:
        str: The corrected sentence.
    """
    messages = [
        {
            "role": "user",
            "content": f"Identify and fix any grammar errors in the following sentence '{sentence}'. If the sentence is already correct, say nothing to fix. Provide the corrected version in plain text without additional explanations. Return only corrected sentence."
        }
    ]

    response_text = await make_httpx_request(api_key, messages)
    final_answer = parse_AI_response(response_text, messages)

    # Extract the corrected texts from the response
    original_text, corrected_text = await asyncio.to_thread(highlight_corrections, sentence, final_answer)

    return original_text, corrected_text

async def paraphrase(sentence : str, api_key : str, context: str = 'casual') -> list:
    """
    Paraphrase a sentence in a specific context and provide five different examples.

    Args:
        sentence (str): The sentence to paraphrase.
        api_key (str): The API key for the Hugging Face model.
        context (str): The context in which to paraphrase the sentence (e.g., casual, formal, academic).
    Returns:
        list: The paraphrased sentence list with five different examples.
    """
    messages = [
        {
            "role": "user",
            "content": f"Paraphrase the following sentence in a {context} way '{sentence}'. Give me five different examples and provide only examples, in plain text without additional explanations. Lastly number the examples."
        }
    ]

    response_text = await make_httpx_request(api_key, messages)
    final_answer = parse_AI_response(response_text, messages)

    # Ensure the final answer is clean and does not contain any tags
    final_answer = await asyncio.to_thread(extract_paraphrase_sentences, final_answer)
    return final_answer

async def compare_words(word_1 : str, word_2 : str, api_key : str) -> str:

    """
    Compare two words and provide examples of how each word is used in a sentence.
    Args:
        word_1 (str): The first word to compare.
        word_2 (str): The second word to compare.
        api_key (str): The API key for the Hugging Face model.
    Returns:
        str: The comparison of the two words with examples
    """

    messages = [
        {
            "role": "user",
            "content": f"Compare the words '{word_1}' and '{word_2}'. Explain their similarities and differences. Provide example sentences for each. Format the response as valid JSON with the following structure: {{ \"similarities\": \"...\", \"differences\": \"...\", \"examples_word1\": [\"...\"], \"examples_word2\": [\"...\"] }}."
        }
    ]

    response_text = await make_httpx_request(api_key, messages, parameters={
        'temperature': 0.2,
    })
    final_answer = parse_AI_response(response_text, messages)

    return final_answer