class OAuthExpiredError(Exception):
    """Raised when OAuth credentials have expired and need to be refreshed."""

    pass


class OAuthScopeChangedError(Exception):
    """Raised when the requested OAuth scopes don't match what the user has previously authorized."""

    pass
