class ReplicateService:
    """
    Replicate API provider (for open models).

    Args:
        api_key (str): Your Replicate API token.
        model (str): Model version string.
        temperature (float, optional): Sampling temperature.
        max_tokens (int, optional): Maximum tokens in output.

    Example:
        ReplicateService(api_key="...", model="replicate/llama-2-7b")
    """
    def __init__(self, api_key, model, temperature=0.7, max_tokens=1024):
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
        Generate a response from Replicate API.

        Args:
            prompt (str): The prompt to send to the LLM.
            result_object (type, optional): If provided, instructs the LLM to return a JSON matching this schema and parses the result into the object.
            **kwargs: Additional parameters for the LLM API.

        Returns:
            str or result_object: The LLM response as a string, or an instance of result_object if provided.
        """
        from ._import_utils import require_package
        from ._response_mapper import map_llm_response
        requests = require_package('requests', extra='requests')
        api_url = f"https://api.replicate.com/v1/predictions"
        headers = {"Authorization": f"Token {self.api_key}"}
        payload = {"input": {"prompt": prompt, **kwargs}, "version": self.model}
        # If result_object is provided, instruct the LLM to return JSON
        if result_object is not None:
            if hasattr(result_object, '__annotations__'):
                fields = ', '.join(f'"{k}": <{v.__name__}>' for k, v in result_object.__annotations__.items())
                schema = f'{{{fields}}}'
            else:
                schema = str(result_object)
            payload["input"]["prompt"] = f"{prompt}\nReturn the result as a JSON object matching this schema: {schema}"
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # Replicate returns output in 'output' key
        return map_llm_response(result, result_object)
