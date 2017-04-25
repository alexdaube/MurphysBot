class UndefineIslandTypeError(RuntimeError):
    def __init__(self, message="Undefine island type", error=None):
        super(UndefineIslandTypeError, self).__init__(message, error)
