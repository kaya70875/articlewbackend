import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
from utils.helpers import extract_paraphrase_sentences

def test_extract_paraphrase_sentences():
    # Test case 1: Paraphrase with a default results
    expected_result_list = [
        "This is the first sentence.",
        "This is the second sentence.",
        "This is the third sentence.",
        "This is the fourth sentence.",
        "This is the fifth sentence."
    ]

    results = "1. This is the first sentence. 2. This is the second sentence. 3. This is the third sentence. 4. This is the fourth sentence. 5. This is the fifth sentence."
    num_sentences = 5

    func_results = extract_paraphrase_sentences(results, num_sentences)
    assert func_results == expected_result_list

def test_extract_paraphrase_sentences_with_custom_num_sentences():
    # Test case 2: Paraphrase with a custom number of sentences
    expected_result_list = [
        "This is the first sentence?",
        "This is the second sentence?",
        "This is the third sentence?",
        "This is the fourth sentence?",
        "This is the fifth sentence?",
        "This is the sixth sentence?",
        "This is the seventh sentence?",
    ]

    results = "1. This is the first sentence? 2. This is the second sentence? 3. This is the third sentence? 4. This is the fourth sentence? 5. This is the fifth sentence? 6. This is the sixth sentence? 7. This is the seventh sentence?"
    num_sentences = 7

    func_results = extract_paraphrase_sentences(results, num_sentences)
    assert func_results == expected_result_list

def test_extract_paraphrase_sentences_with_single_sentence():
    # Test case 3: Paraphrase with a single sentence
    expected_result_list = [
        "This is the single sentence."
    ]
    results = "1. This is the single sentence."
    num_sentences = 1

    func_results = extract_paraphrase_sentences(results, num_sentences)
    assert func_results == expected_result_list

def test_extract_paraphrase_sentences_with_zero_sentences():
    # Test case 4: Paraphrase with zero sentences
    expected_result_list = []
    results = ""
    num_sentences = 0

    func_results = extract_paraphrase_sentences(results, num_sentences)
    assert func_results == expected_result_list

def test_extract_paraphrase_sentences_with_wrong_ai_response():
    # Test case 5: Paraphrase with a wrong AI response
    results = "This is a wrong AI response."
    num_sentences = 1

    with pytest.raises(ValueError, match="AI Agent response is not correct. Please check your prompt."):
        extract_paraphrase_sentences(results, num_sentences)
