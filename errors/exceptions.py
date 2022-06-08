class AppBackendError(Exception):
    def __init__(self, message) -> 'AppBackendError':
        super().__init__(message)

class UnknownIdError(AppBackendError):
    """
    """
    def __init__(self, _id: int):
        self.message = {'message': f"Object with id = '{_id}' wasn't found"}
        super().__init__(self.message)