import requests


class AccountApi:
    def __init__(self, url=None,header=None):
        self.url = f"{url}:7017/api/Account"
        if header:
            self.headers=header
        else:
            self.headers = {'accept': 'application/json'}
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def post_register(self, register):
        res = self.session.post(url=f"{self.url}/register", json=register.to_json())
        return res

    def post_login(self, login):
        res = self.session.post(url=f"{self.url}/login", json=login.to_json())
        return res

    def post_refreshtoken(self, refreshtoken):
        res = self.session.post(url=f"{self.url}/refreshtoken", json=refreshtoken.to_json())
        return res

    def refresh_header(self, header):
        self.session.headers.update(header)
        return self

