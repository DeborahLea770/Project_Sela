from API.models.BaseObj import BaseObj

class LoginDto(BaseObj):
    def __init__(self, email: str, password: str):
        self._email = None
        self._password = None

        if not isinstance(email, str):
            raise TypeError("email must be string")
        self._email = email

        if not isinstance(password, str):
            raise TypeError("password must be string")
        if 4 > len(password) > 15:
            raise TypeError("password must be between 4-15 char")
        self._password = password

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = password


