import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.utils.text_helpers import extract_sentence

def test_extract_sentence():
    # Test case 1: Test default behavior
    results = [{'text': 'Hi, I am ahmet. He was visited by his friends and family.'}, {'text': 'He visited me today.'}]
    word = 'visited'

    expected_output = [{'text': 'He was visited by his friends and family.'}, {'text': 'He visited me today.'}]
    func_results = extract_sentence(results, word)

    assert func_results == expected_output

def test_extract_sentence_with_excessive_spaces():
    # Test case 2: Test with excessive spaces
    results = [{'text': 'Hi, I am ahmet     .         He was visited by his friends and family.'}]
    word = 'visited'

    expected_output = [{'text': 'He was visited by his friends and family.'}]
    func_results = extract_sentence(results, word)

    assert func_results == expected_output

def test_extract_sentence_with_related_shortened_verb():
    # Test case 3: Test with related shortened verbs
    results = [{'text': 'Hi, I am ahmet. He was visited by his friends and family.'}]
    word = 'visit'

    expected_output = [{'text': ''}]
    func_results = extract_sentence(results, word)

    assert func_results == expected_output

def test_extract_sentence_with_same_word_in_sentence():
    # Test case 4: Test with new lines
    results = [{'text': 'He was visited by his friends and family and visited by his girlfriend which is pretty cool.'}]
    word = 'visited'

    expected_output = [{'text': 'He was visited by his friends and family and visited by his girlfriend which is pretty cool.'}]
    func_results = extract_sentence(results, word)

    assert func_results == expected_output