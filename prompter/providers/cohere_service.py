class CohereService:
    """
    Cohere provider.

    Args:
        api_key (str): Your Cohere API key.
        model (str): Model name, e.g. 'command', 'command-r'.
        temperature (float, optional): Sampling temperature.
        max_tokens (int, optional): Maximum tokens in output.

    Example:
        CohereService(api_key="...", model="command")
    """
    def __init__(self, api_key, model="command", temperature=0.7, max_tokens=1024):
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
        Generate a response from Cohere.

        Args:
            prompt (str): The prompt to send to the LLM.
            result_object (type, optional): If provided, instructs the LLM to return a JSON matching this schema and parses the result into the object.
            **kwargs: Additional parameters for the LLM API.

        Returns:
            str or result_object: The LLM response as a string, or an instance of result_object if provided.
        """
        from ._import_utils import require_package
        from ._response_mapper import map_llm_response
        cohere = require_package('cohere', extra='cohere')
        client = cohere.Client(self.api_key)
        response = client.generate(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        # Cohere returns generations[0].text as the main output
        result = {"text": response.generations[0].text}
        return map_llm_response(result, result_object)
