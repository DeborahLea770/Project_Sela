import requests


class BookApi:
    def __init__(self, url=None,header=None):
        self.url = f"{url}:7017/api/Books"
        if header:
            self.headers=header
        else:
            self.headers = {'accept': 'application/json'}
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def get_books(self):
        res = self.session.get(url=f"{self.url}")
        return res

    def post_book(self,book):
        res = self.session.post(url=f"{self.url}", json=book.to_json())
        return res

    def get_book_byid(self,id:int):
         res = self.session.get(url=f"{self.url}/{id}")
         return res

    def put_book_byid(self,id:int,updatebook):
        res = self.session.put(url=f"{self.url}/{id}",json=updatebook.to_json())
        return res

    def delete_book_byid(self,id:int):
        res = self.session.delete(url=f"{self.url}/{id}")
        return res

    def get_books_by_author_id(self,authorid:int):
        res = self.session.get(url=f"{self.url}/findauthor/{authorid}")
        return res

    def put_book_purchase_byid(self,id:int):
        res = self.session.put(url=f"{self.url}/purchase/{id}")
        return res