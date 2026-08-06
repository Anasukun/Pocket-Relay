class PocketRelayError(Exception):
    """Base error for PocketRelay"""

class AuthDeniedError(PocketRelayError):
    pass

class ProjectNotFoundError(PocketRelayError):
    pass
