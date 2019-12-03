class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, code=None, expression=None, message=None):
        self.expression = expression
        self.message = message
        self.code = code


class ValidationError(Error):
    """Exception raised for errors in the validator.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, code=None, expression=None, message=None):
        self.expression = expression
        self.message = message
        self.code = code
