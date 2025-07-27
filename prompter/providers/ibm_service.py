class IBMWatsonService:
    """
    IBM watsonx.ai provider.

    Args:
        api_key (str): Your IBM Cloud API key.
        project_id (str): IBM Cloud project ID.
        model (str): Model name.
        temperature (float, optional): Sampling temperature.
        max_tokens (int, optional): Maximum tokens in output.

    Example:
        IBMWatsonService(api_key="...", project_id="...", model="ibm/granite-13b-chat-v2")
    """
    def __init__(self, api_key, project_id, model, temperature=0.7, max_tokens=1024):
        self.api_key = api_key
        self.project_id = project_id
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
        Generate a response from IBM watsonx.ai.

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
        api_url = f"https://{self.project_id}.watsonx.ai.ibm.com/v1/generate"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"prompt": prompt, "model": self.model, "temperature": self.temperature, "max_tokens": self.max_tokens}
        payload.update(kwargs)
        # If result_object is provided, instruct the LLM to return JSON
        if result_object is not None:
            if hasattr(result_object, '__annotations__'):
                fields = ', '.join(f'"{k}": <{v.__name__}>' for k, v in result_object.__annotations__.items())
                schema = f'{{{fields}}}'
            else:
                schema = str(result_object)
            payload["prompt"] = f"{prompt}\nReturn the result as a JSON object matching this schema: {schema}"
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return map_llm_response(result, result_object)
