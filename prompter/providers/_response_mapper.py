import json
from typing import Any, Type

def map_llm_response(
    result: dict,
    result_object: Type = None,
    keys = ("text", "output", "response", "result")
) -> Any:
    """
    Map a raw LLM API response dict to a string or a result object.

    Args:
        result (dict): The response dict from the LLM API.
        result_object (type, optional): If provided, parse the response as this type.
        keys (tuple): Keys to check for the main output.

    Returns:
        str or result_object: The mapped response.
    """
    for key in keys:
        if key in result:
            value = result[key]
            if result_object is not None:
                if isinstance(value, str):
                    value = json.loads(value)
                if hasattr(result_object, '__annotations__'):
                    return result_object(**value)
                return value
            return value
    return str(result)
