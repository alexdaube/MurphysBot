class NoPathFoundError(RuntimeError):
    def __init__(self, message="No path found", error=None):
        super(NoPathFoundError, self).__init__(message, error)
