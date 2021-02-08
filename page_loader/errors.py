class KnownError(Exception):
    pass


class DownloadingError(KnownError):
    pass


class SavingError(KnownError):
    pass
