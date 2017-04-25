class OutOfMapBoundariesError(RuntimeError):
    def __init__(self, message="Out of map boundaries", error=None):
        super(OutOfMapBoundariesError, self).__init__(message, error)
