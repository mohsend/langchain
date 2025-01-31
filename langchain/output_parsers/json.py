from __future__ import annotations

import json
from typing import List

from langchain.schema import OutputParserException

def remove_text_before_json(input_string: str) -> str:
    index = input_string.find("```")
    if index !=-1 :
            return input_string[index:] 
    return input_string

def parse_json_markdown(json_string: str) -> dict:
    # Remove any string before the json response
    json_string = remove_text_before_json(json_string)
    
    # Remove the triple backticks if present
    json_string = json_string.replace("```json", "").replace("```", "")

    # Strip whitespace and newlines from the start and end
    json_string = json_string.strip()

    # Parse the JSON string into a Python dictionary
    parsed = json.loads(json_string)

    return parsed


def parse_and_check_json_markdown(text: str, expected_keys: List[str]) -> dict:
    try:
        json_obj = parse_json_markdown(text)
    except json.JSONDecodeError as e:
        raise OutputParserException(f"Got invalid JSON object. Error: {e}")
    for key in expected_keys:
        if key not in json_obj:
            raise OutputParserException(
                f"Got invalid return object. Expected key `{key}` "
                f"to be present, but got {json_obj}"
            )
    return json_obj
