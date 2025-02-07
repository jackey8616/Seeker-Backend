from typing import Annotated

from google.auth.external_account_authorized_user import Credentials as extCredentials
from google.oauth2.credentials import Credentials as oauth2Credentials
from pydantic import BeforeValidator

type GoogleOAuthCredentials = extCredentials | oauth2Credentials
type PyObjectId = Annotated[str, BeforeValidator(str)]
