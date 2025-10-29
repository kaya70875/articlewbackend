import re
from difflib import SequenceMatcher
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def extract_sentences_from_raw_text(results : list, word: str) -> list[str]:

    """
    Extract the sentence that contains the word. This function extract sentences from a text or sentence using a regular expression.

    Args:
        results (list): The text or sentence to search for the word.
        word (str): The word to search for in the text.
    
    Returns:
        list: The list of extracted sentences.
    """

    regex = rf'\b[A-Z][^.!?]*?\b{word}\b[^.!?]*[.!?]'
    new_results = []
    
    for text in results:
        extracted_sentences = re.findall(regex, text['text'], re.IGNORECASE)
        new_text = ' '.join(extracted_sentences)
        new_text_dict = {**text, 'text': new_text}  # Preserve other fields and update 'text'
        new_results.append(new_text_dict)
        
    return new_results

def highlight_corrections(original : str, corrected : str) -> tuple[str, str]:

    """
    Highlights the differences between the two texts. First one highlighted as red, second one highlighted as green.

    Args:
        original (str): The original text that user input.
        corrected (str): The corrected text from AI Agent.
    
    Returns:
        str: The original text with highlighted differences.
        str: The corrected text with highlighted differences.
    """

    # Use SequenceMatcher to find differences
    matcher = SequenceMatcher(None, original.split(), corrected.split())
    
    original_highlighted = []
    corrected_highlighted = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":  # Words replaced
            original_text = " ".join(original.split()[i1:i2])
            corrected_text = " ".join(corrected.split()[j1:j2])
            original_highlighted.append(f"<span style='color:#E76047; font-weight:bold;'>{original_text}</span>")
            corrected_highlighted.append(f"<span style='color:#69B23E; font-weight:bold;'>{corrected_text}</span>")
        elif tag == "delete":  # Words deleted in corrected version
            original_text = " ".join(original.split()[i1:i2])
            original_highlighted.append(f"<span style='color:#E76047; font-weight:bold;'>{original_text}</span>")
        elif tag == "insert":  # Words inserted in corrected version
            corrected_text = " ".join(corrected.split()[j1:j2])
            corrected_highlighted.append(f"<span style='color:#69B23E; font-weight:bold;'>{corrected_text}</span>")
        elif tag == "equal":  # No changes
            unchanged_text = " ".join(original.split()[i1:i2])
            original_highlighted.append(unchanged_text)
            corrected_highlighted.append(unchanged_text)
    
    return " ".join(original_highlighted), " ".join(corrected_highlighted)

def extract_paraphrase_sentences(results : str, num_sentences : int = 5) -> list:

    """
    Extract the five paraphrased sentences from the raw text and put it into a list.

    Args:
        results (str): The raw text containing the paraphrased sentences. This text coming from AI Agent.
        num_sentences (int, optional): The number of sentences to extract. Defaults to 6 means 5 sentences. You should also change AI Agent response to return sentences you want to get.
    Returns:
        list: List of paraphrased sentences.
    """

    extracted_list = []
    for i in range(1,num_sentences + 1):
        if(results[0] != "1"):
            raise ValueError("AI Agent response is not correct. Please check your prompt.")
        find_first = results.find(f"{i}.")
        find_next = results.find(f"{i + 1}.") if i < num_sentences else None
        extract = results[find_first + 3:find_next].strip()
        
        extracted_list.append(extract)
    
    return extracted_list
        
def parse_AI_response(response_text : str , messages) -> str:

    """
    Parse the AI response and extract the final answer.
    Args:
        response_text (str): The AI response text.
        messages (list): The messages section of AI.
    Returns:
        str: The final answer extracted from the AI response.
    
    """
    if not messages[0]["content"]:
        logger.error("No messages found in the AI response")
        raise ValueError("No messages found in the response")

    if "<think>" or "</think>" in response_text:
        # Split the response text at "</think>" and take the last part
        final_answer = response_text.split("</think>")[-1].strip()
        
        # Remove any remaining tags or unwanted text
        final_answer = final_answer.replace("<think>", "").strip()
    else:
        final_answer = response_text.strip()

    # Ensure the final answer is clean and does not contain any tags
    final_answer = final_answer.replace("</think>", "").strip().replace(messages[0]["content"], "")
    return final_answer