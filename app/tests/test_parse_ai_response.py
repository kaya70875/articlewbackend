import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
from utils.helpers import parse_AI_response

def test_no_message_content():
    messages = [{'content': ''}]
    response_text = 'any response'
    with pytest.raises(ValueError, match="No messages found in the response"):
        parse_AI_response(response_text, messages)

def test_response_with_think_tags():
    messages = [{'content': 'Original message'}]
    response_text = f"{messages[0]['content']} <think>Some thinking output</think> Final answer"

    result = parse_AI_response(response_text, messages)
    assert result == 'Final answer'

def test_response_without_think_tags():
    messages = [{'content': 'Original message'}]
    response_text = "Final answer"

    result = parse_AI_response(response_text, messages)
    assert result == "Final answer"

def test_response_with_multiple_think_tags():
    messages = [{'content': 'Original message'}]
    response_text = f"{messages[0]['content']} <think>Some thinking output</think> <think>Another thinking output</think> Final answer"

    result = parse_AI_response(response_text, messages)
    assert result == 'Final answer'