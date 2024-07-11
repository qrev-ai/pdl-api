
class PDLException(Exception):
    def __init__(self, response: dict[str, str], message: str, **kwargs):
        self.response = response
        super().__init__(message, **kwargs)

class PDLAccountLimitException(PDLException):
    pass

class PDLUnknownException(PDLException):
    pass
