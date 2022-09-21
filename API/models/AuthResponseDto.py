from API.models.BaseObj import BaseObj

class AuthResponseDto(BaseObj):
    def __init__(self, userId: str, token: str, refreshToken:str):
        self._userId = None
        self._token = None
        self._refreshToken = None

        if not isinstance(userId, str):
            raise TypeError("id must be string")
        self._userId = userId

        if not isinstance(token, str):
            raise TypeError("token must be string")
        self._token = token

        if not isinstance(refreshToken, str):
            raise TypeError("refreshToken must be string")
        self._refreshToken = refreshToken

    @property
    def userId(self):
        return self._userId

    @property
    def token(self):
        return self._token

    @property
    def refreshToken(self):
        return self._refreshToken

    @userId.setter
    def userId(self, userId: str):
        self._userId = userId

    @token.setter
    def token(self, token: str):
        self._token = token

    @refreshToken.setter
    def refreshToken(self, refreshToken: str):
        self._refreshToken = refreshToken

