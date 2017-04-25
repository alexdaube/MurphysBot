class NoMatchingPointOfInterestError(RuntimeError):
    def __init__(self, message="No matching point of interest found", error=None):
        super(NoMatchingPointOfInterestError, self).__init__(message, error)
