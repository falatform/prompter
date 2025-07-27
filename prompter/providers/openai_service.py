class OpenAIService:
    """
    OpenAI GPT-3/4 provider.

    Args:
        api_key (str): Your OpenAI API key.
        model (str): Model name, e.g. 'gpt-4', 'gpt-3.5-turbo'.
        base_url (str, optional): Custom base URL for OpenAI-compatible endpoints.
        organization (str, optional): OpenAI organization ID.
        temperature (float, optional): Sampling temperature.
        max_tokens (int, optional): Maximum tokens in output.

    Example:
        OpenAIService(api_key="sk-...", model="gpt-4")
    """
    def __init__(self, api_key, model="gpt-4", base_url=None, organization=None, temperature=0.7, max_tokens=1024):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.organization = organization
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
        Generate a response from OpenAI.

        Args:
            prompt (str): The prompt to send to the LLM.
            result_object (type, optional): If provided, instructs the LLM to return a JSON matching this schema and parses the result into the object.
            **kwargs: Additional parameters for the LLM API.

        Returns:
            str or result_object: The LLM response as a string, or an instance of result_object if provided.
        """
        from ._import_utils import require_package
        from ._response_mapper import map_llm_response
        openai = require_package('openai', extra='openai')
        params = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        params.update(kwargs)
        if self.base_url:
            openai.base_url = self.base_url
        if self.organization:
            openai.organization = self.organization
        openai.api_key = self.api_key
        # If result_object is provided, instruct the LLM to return JSON
        if result_object is not None:
            if hasattr(result_object, '__annotations__'):
                fields = ', '.join(f'"{k}": <{v.__name__}>' for k, v in result_object.__annotations__.items())
                schema = f'{{{fields}}}'
            else:
                schema = str(result_object)
            params["messages"][0]["content"] = f"{prompt}\nReturn the result as a JSON object matching this schema: {schema}"
        response = openai.ChatCompletion.create(**params)
        # OpenAI returns choices[0]["message"]["content"] as the main output
        result = {"text": response["choices"][0]["message"]["content"]}
        return map_llm_response(result, result_object)
