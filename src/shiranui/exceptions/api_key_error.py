class ApiKeyError(Exception):
    """Exception raised when the API key is missing."""
    def __init__(self, message="API key is required"):
        self.message = message
        super().__init__(self.message)
