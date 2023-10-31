class APIError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AlreadyProcessedError(Exception):
    """
    Is raised when a request did not require authentication to complete.
    
    It is highly recommended that you wrap your functions in a 
    
    try: 
        *
    except AlreadyProcessedError:
    
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
