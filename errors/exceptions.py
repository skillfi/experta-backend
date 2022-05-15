class ExpertaBackendError(Exception):
    def __init__(self, message) -> 'ExpertaBackendError':
        super().__init__(message)

class UnknownCoollectionIdError(ExpertaBackendError):
    """
    """
    def __init__(self, _id: int, collection: str):
        self.message = {'message': f"Object with id = '{_id}' wasn't found"}
        super().__init__(self.message)