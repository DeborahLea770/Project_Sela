import requests


class AuthorsApi:
    def __init__(self, url=None,header=None):
        self.url = f"{url}:7017/api/Authors"
        if header:
            self.headers=header
        else:
            self.headers = {'accept': 'application/json'}
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def get_authors(self):
        res = self.session.get(url=f"{self.url}")
        return res


    def post_authors(self,author):
        res = self.session.post(url=f"{self.url}",json=author.to_json())
        return res

    def get_author_id(self, id:int):
        res = self.session.get(url=f"{self.url}/{id}")
        return res

    def put_author_byid(self, id:int,updateauthor):
        res = self.session.put(url=f"{self.url}/{id}",json=updateauthor.to_json())
        return res

    def delete_authors_id(self, authorsid):
        res = self.session.delete(url=f"{self.url}/{authorsid}")
        return res

    def get_authors_search_txt(self, txt:str):
        res = self.session.get(url=f"{self.url}/search/{txt}")
        return res