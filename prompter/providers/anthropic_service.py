class AnthropicService:
    """
    Anthropic Claude provider (direct API).

    Args:
        api_key (str): Your Anthropic API key.
        model (str): Model name, e.g. 'claude-3-opus-20240229'.
        temperature (float, optional): Sampling temperature.
        max_tokens (int, optional): Maximum tokens in output.

    Example:
        AnthropicService(api_key="...", model="claude-3-opus-20240229")
    """
    def __init__(self, api_key, model="claude-3-opus-20240229", temperature=0.7, max_tokens=1024):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    def generate(
        self,
        prompt: str,
        *,
        result_object: type = None,
        **kwargs
    ) -> str:
        """
        Generate a response from Anthropic Claude.

        Args:
            prompt (str): The prompt to send to the LLM.
            result_object (type, optional): If provided, instructs the LLM to return a JSON matching this schema and parses the result into the object.
            **kwargs: Additional parameters for the LLM API.

        Returns:
            str or result_object: The LLM response as a string, or an instance of result_object if provided.
        """
        from ._import_utils import require_package
        from ._response_mapper import map_llm_response
        anthropic = require_package('anthropic', extra='anthropic')
        client = anthropic.Anthropic(api_key=self.api_key)
        # If result_object is provided, instruct the LLM to return JSON
        user_content = prompt
        if result_object is not None:
            if hasattr(result_object, '__annotations__'):
                fields = ', '.join(f'"{k}": <{v.__name__}>' for k, v in result_object.__annotations__.items())
                schema = f'{{{fields}}}'
            else:
                schema = str(result_object)
            user_content = f"{prompt}\nReturn the result as a JSON object matching this schema: {schema}"
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": user_content}],
            **kwargs
        )
        # Anthropic returns content[0].text as the main output
        content = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
        result = {"text": content}
        return map_llm_response(result, result_object)
