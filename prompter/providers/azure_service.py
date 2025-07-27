class AzureOpenAIService:
    """
    Azure OpenAI provider.

    Args:
        api_key (str): Your Azure OpenAI API key.
        endpoint (str): Azure OpenAI endpoint URL.
        deployment (str): Deployment name for your model.
        model (str, optional): Model name (optional, for some endpoints).
        api_version (str, optional): API version string.
        temperature (float, optional): Sampling temperature.
        max_tokens (int, optional): Maximum tokens in output.

    Example:
        AzureOpenAIService(api_key="...", endpoint="https://...", deployment="gpt-4")
    """
    def __init__(self, api_key, endpoint, deployment, model=None, api_version=None, temperature=0.7, max_tokens=1024):
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment = deployment
        self.model = model
        self.api_version = api_version
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
        Generate a response from Azure OpenAI.

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
        openai.api_type = "azure"
        openai.api_key = self.api_key
        openai.api_base = self.endpoint
        if self.api_version:
            openai.api_version = self.api_version
        params = {
            "engine": self.deployment,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        params.update(kwargs)
        # If result_object is provided, instruct the LLM to return JSON
        if result_object is not None:
            if hasattr(result_object, '__annotations__'):
                fields = ', '.join(f'"{k}": <{v.__name__}>' for k, v in result_object.__annotations__.items())
                schema = f'{{{fields}}}'
            else:
                schema = str(result_object)
            params["messages"][0]["content"] = f"{prompt}\nReturn the result as a JSON object matching this schema: {schema}"
        response = openai.ChatCompletion.create(**params)
        # Azure OpenAI returns choices[0]["message"]["content"] as the main output
        result = {"text": response["choices"][0]["message"]["content"]}
        return map_llm_response(result, result_object)
