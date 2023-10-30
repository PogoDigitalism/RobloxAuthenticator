class APIError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AlreadyProcessedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
