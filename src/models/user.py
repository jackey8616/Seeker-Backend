from models import MongoDocument
from services.google.oauth.dtos.google_credentials import GoogleCredentials
from services.google.oauth.dtos.google_user_info import GoogleUserInfo


class ModelUser(MongoDocument):
    google_userinfo: GoogleUserInfo
    google_credentials: GoogleCredentials
