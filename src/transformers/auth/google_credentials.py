from datetime import datetime
from typing import cast

from dtos.google.credentials import GoogleCredentials
from utils.typings import GoogleOAuthCredentials


class GoogleCredentialsTransformer:
    def transform(self, data: GoogleOAuthCredentials) -> GoogleCredentials:
        assert data.token is not None
        assert data.refresh_token is not None
        assert data.expired is not None

        return GoogleCredentials(
            token=data.token,
            refresh_token=data.refresh_token,
            expiry=cast(datetime, data.expiry),
        )
