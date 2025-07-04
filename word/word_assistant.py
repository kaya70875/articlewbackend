from app.utils.request_helpers import get_chat_completion
from app.utils.text_helpers import *
import asyncio

class WordAssistant:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def analyze_word(self, word: str) -> str:
        """
        Analyze a word and provide an example of its usage in a sentence. 
        Additionally checks if word itself is correct or not in writing English.

        Args:
            word (str): The word to analyze.
            api_key (str): The API key for the Hugging Face model.
        Returns:
            str: The analysis of the word with an example sentence.
        """
        content = {
                "role": "user",
                "content": f"Analyze '{word}' and give an example of its usage. Return a json like this: {{\"check\": \"'prevent' is a correct and usable word in written English.\",\"analysis\" : \"It can be used to describe a situation in which something bad is avoided from happening. For example: 'Taking precautions helped us prevent the spread of the virus.'\"}}"
            }

        response_text = await asyncio.to_thread(get_chat_completion, self.api_key, content, 1.3, 'json_object')
        return response_text
    
    async def fix_grammar_errors(self, sentence : str) -> tuple[str, str]:
        """
        Identify and fix any grammar errors in a sentence. If the sentence is already correct, return the original sentence.

        Args:
            sentence (str): The sentence to correct.
            api_key (str): The API key for the Hugging Face model.
        Returns:
            str: The corrected sentence.
        """
        
        content = {
                "role": "user",
                "content": f"Identify and fix any grammar errors for '{sentence}'. If the sentence is already correct, say nothing to fix. Provide the corrected version in plain text without additional explanations. Return only corrected sentence."
        }

        response_text = await asyncio.to_thread(get_chat_completion, self.api_key, content)

        # Extract the corrected texts from the response
        original_text, corrected_text = await asyncio.to_thread(highlight_corrections, sentence, response_text)

        return original_text, corrected_text, response_text # TIP: Return response_text as plain text so we do not have to extract span contents from our frontend.
    async def paraphrase(self, sentence : str, context: str = 'casual') -> list:
        """
        Paraphrase a sentence in a specific context and provide five different examples.

        Args:
            sentence (str): The sentence to paraphrase.
            api_key (str): The API key for the Hugging Face model.
            context (str): The context in which to paraphrase the sentence (e.g., casual, formal, academic).
        Returns:
            list: The paraphrased sentence list with five different examples.
        """
        content = {
                "role": "user",
                "content": f"Paraphrase '{sentence}' in a {context} way. Return five different examples in plain text without additional explanations. Lastly number the examples."
            }

        response_text = await asyncio.to_thread(get_chat_completion, self.api_key, content)

        # Ensure the final answer is clean and does not contain any tags
        final_answer = await asyncio.to_thread(extract_paraphrase_sentences, response_text)
        return final_answer
    
    async def compare_words(self, word_1 : str, word_2 : str) -> str:
        """
        Compare two words and provide examples of how each word is used in a sentence.
        Args:
            word_1 (str): The first word to compare.
            word_2 (str): The second word to compare.
            api_key (str): The API key for the Hugging Face model.
        Returns:
            str: The comparison of the two words with examples
        """

        content = {
                "role": "user",
                "content": f"Compare '{word_1}' and '{word_2}'. Explain their similarities and differences. Format the response as valid JSON with the following structure: {{ \"similarities\": \"...\", \"differences\": \"...\", \"examples_word1\": [\"...\"], \"examples_word2\": [\"...\"] }}."
            }

        response_text = await asyncio.to_thread(get_chat_completion, self.api_key, content, 1.3, 'json_object')
        return response_text