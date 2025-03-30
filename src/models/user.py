from dtos.google.credentials import GoogleCredentials
from dtos.google.userinfo import GoogleUserInfo
from models import MongoDocument


class ModelUser(MongoDocument):
    google_userinfo: GoogleUserInfo
    google_credentials: GoogleCredentials
