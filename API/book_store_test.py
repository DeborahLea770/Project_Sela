import  logging
import random
import requests

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()

from API.api.account_api import AccountApi
from API.api.authors_api import AuthorsApi
from API.api.books_api import BookApi

from API.conftest import *
from API.models.LoginDto import LoginDto
from API.models.ApiUserDto import ApiUserDto
from API.models.AuthResponseDto import AuthResponseDto
from API.models.AuthorsDto import AuthorsDto
from API.models.CreateBookDto import CreateBookDto
from API.models.CreateAuthorDto import CreateAuthorDto
from API.models.UpdateAuthorDto import UpdateAuthorDto
from API.models.BookDto import BookDto


userId= "a980b8c6-ccac-4cc7-8959-3044e0f30b77"

@pytest.fixture()
def Bearer_Author(My_User,url_config):
    My_Register = ApiUserDto("deborahlea770@gmail.com", "123456", "deborah", "fellous")
    requests.post(f'{url_config}:7017/api/Account/register',json=My_Register.to_json())
    res_login = requests.post(f'{url_config}:7017/api/Account/login',json=My_User.to_json())
    token = res_login.json()["token"]
    HEADERS = {'Authorization': f'Bearer {token}'}
    return HEADERS

@pytest.fixture()
def Api_Account(Bearer_Author, url_config):
    accountApi = AccountApi(url_config,header=Bearer_Author)
    return accountApi

@pytest.fixture()
def Api_Author(Bearer_Author, url_config):
    authorsApi = AuthorsApi(url_config,header=Bearer_Author)
    return authorsApi

@pytest.fixture()
def Api_Book(Bearer_Author, url_config):
    bookApi = BookApi(url_config,header=Bearer_Author)
    return bookApi

@pytest.fixture()
def My_New_Register() -> ApiUserDto:
    email = "a%@gmail.com"
    num = random.randint(0, 1000)
    email = email.replace("%",str(num))
    reg = ApiUserDto(email,"123456","deborah","fellous")
    return reg

@pytest.fixture()
def My_Register() -> ApiUserDto:
    res = ApiUserDto("deborahlea770@gmail.com","123456","deborah","fellous")
    return res

@pytest.fixture()
def My_User() -> LoginDto:
    user = LoginDto("deborahlea770@gmail.com","123456")
    return user

@pytest.fixture()
def My_Author() -> AuthorsDto :
    author = AuthorsDto("George Orwell",26.643,84.91426,CreateBookDto("Animal Farm", "Animal Farm is a beast fable, in form of satirical allegorical novellaby George Orwell",
                                           50,7,"https://images-na.ssl-images-amazon.com/images/I/91LUbAcpACL.jpg",1))
    return author

# @pytest.fixture()
def My_New_Book(Author_id) -> CreateBookDto :
    book = CreateBookDto("harry potter","aaaa",50,10,"https://m.media-amazon.com/images/I/91BT--NUiKL._AC_UY218_.jpg",Author_id)
    return book

@pytest.fixture()
def My_New_Author() -> CreateAuthorDto:
    new_author = CreateAuthorDto("deborah",12.3,12.4)
    return new_author

def Authors_id(res) -> list:
    authors_id = []
    for author in res.json():
        authors_id.append(author["id"])
    return authors_id

def Books_id(res)-> list:
    books_id = []
    for book in res.json():
        books_id.append(book["id"])
    return books_id





################ ACCOUNT
### post register
def test_post_register(My_New_Register, Api_Account):
    mylogger.info("test for post register")
    res_post_register = Api_Account.post_register(My_New_Register)
    assert res_post_register.status_code == 200

def test_post_register_empty_invalid_email(My_New_Register, Api_Account):
    mylogger.info("test for empty or invalid register")
    My_New_Register.email= ""
    res_post_register = Api_Account.post_register(My_New_Register)
    assert "The Email field is required." in res_post_register.text
    My_New_Register.email = "aaa@"
    res_post_register = Api_Account.post_register(My_New_Register)
    assert "The Email field is not a valid e-mail address." in res_post_register.text

def test_post_register_invalid_empty_password(My_New_Register, Api_Account):
    mylogger.info("test for empty or invalid password")
    My_New_Register.password= "12"
    res_post_register = Api_Account.post_register(My_New_Register)
    assert "Your password is limited to 4 to 15 characters" in res_post_register.text
    My_New_Register.password = "1234567891234567"
    res_post_register = Api_Account.post_register(My_New_Register)
    assert "Your password is limited to 4 to 15 characters" in res_post_register.text
    My_New_Register.password = ""
    res_post_register = Api_Account.post_register(My_New_Register)
    assert "The Password field is required." in res_post_register.text

def test_post_exist_register_(My_Register, Api_Account):
    mylogger.info("test for exist post register")
    res_post_register = Api_Account.post_register(My_Register)
    assert  f"Username '{My_Register.email}' is already taken." in res_post_register.text

##### post login
def test_post_login(My_User, Api_Account):
    mylogger.info("test for post login")
    res_post_register = Api_Account.post_login(My_User)
    assert userId == res_post_register.json()["userId"]

def test_post_login_empty_invalid_email(My_User, Api_Account):
    mylogger.info("test for empty or invalid email in login")
    My_User.email = ""
    res_post_register = Api_Account.post_login(My_User)
    assert "The Email field is required." in res_post_register.text
    My_User.email = "aa@"
    res_post_register = Api_Account.post_login(My_User)
    assert "The Email field is not a valid e-mail address." in res_post_register.text

def test_post_login_invalid_empty_password(My_User, Api_Account):
    mylogger.info("test for empty or invalid password in login")
    My_User.password = "1234567"
    res_post_register = Api_Account.post_login(My_User)
    assert "Unauthorized"  in res_post_register.text
    My_User.password = ""
    res_post_register = Api_Account.post_login(My_User)
    assert "One or more validation errors occurred." in res_post_register.text
    My_User.password = "123"
    res_post_register = Api_Account.post_login(My_User)
    assert "Your password is limited to 4 to 15 characters" in res_post_register.text
    My_User.password = "1231231231212313123123"
    res_post_register = Api_Account.post_login(My_User)
    assert "Your password is limited to 4 to 15 characters" in res_post_register.text

#### post refrestoken
def test_post_refreshtoken(Api_Account, My_User):
    mylogger.info("test for refreshtoken")
    res_login = Api_Account.post_login(My_User)
    MyToken = AuthResponseDto(**res_login.json())
    res_post_refreshtoken = Api_Account.post_refreshtoken(MyToken)
    assert res_post_refreshtoken.json()["userId"] == res_login.json()["userId"]

def test_post_refreshtoken_invalid_userid_and_refreshtoken(Api_Account, My_User):
    mylogger.info("test for invalid userid and refreshtoken")
    res_login = Api_Account.post_login(My_User)
    MyToken = AuthResponseDto(**res_login.json())
    MyToken.userId = "aaaa"
    res_post_refreshtoken = Api_Account.post_refreshtoken(MyToken)
    assert "Unauthorized" in res_post_refreshtoken.text
    MyToken = AuthResponseDto(**res_login.json())
    MyToken.refreshToken = "aaaa"
    res_post_refreshtoken = Api_Account.post_refreshtoken(MyToken)
    assert "Unauthorized" in res_post_refreshtoken.text

@pytest.mark.skip(reason="the response is allways 500")
def test_post_refreshtoken_invalid_token(Api_Account, My_User, My_Register): ##500
    mylogger.info("test for post refreshtoken with invalid token")
    Api_Account.post_register(My_Register)
    res_login = Api_Account.post_login(My_User)
    MyToken = AuthResponseDto(**res_login.json())
    MyToken.token = "aaaa"
    res_post_refreshtoken = Api_Account.post_refreshtoken(MyToken)
    assert "Unauthorized" in res_post_refreshtoken.text

############################# AUTHORS
#get author
def test_get_authors(Api_Author,My_New_Author):
    mylogger.info("test for get authors")
    Api_Author.post_authors(My_New_Author)
    res_get_authors = Api_Author.get_authors()
    assert My_New_Author.name in res_get_authors.text
#post author
def test_post_author(Api_Author, My_New_Author):
    mylogger.info("test for post author")
    res_post_authors = Api_Author.post_authors(My_New_Author)
    assert  My_New_Author.name == res_post_authors.json()["name"]

def test_post_author_empty_name(Api_Author, My_New_Author):
    mylogger.info("test for post author with emtpy name")
    My_New_Author.name = ""
    res_post_authors = Api_Author.post_authors(My_New_Author)
    assert  "The Name field is required." in res_post_authors.text

# get author by id
def test_get_author_id(Api_Author,My_New_Author):
    mylogger.info("test for get author by id")
    res = Api_Author.get_authors()
    id = res.json()[0]["id"]
    res_get_author_byid = Api_Author.get_author_id(id)
    assert id == res_get_author_byid.json()["id"]

def test_get_author_invalid_or_notexist_id(My_Author, Api_Author):
    mylogger.info("test for get author with invalid or unexist id")
    res_get_author_byid = Api_Author.get_author_id(-1)
    assert "Not Found" in res_get_author_byid.text
    res_get_authors_id = Api_Author.get_authors()
    authors_id = Authors_id(res_get_authors_id)
    while True:
        num = random.randint(0, len(authors_id)+1)
        if num not in authors_id:
           res_get_author_byid = Api_Author.get_author_id(num)
           assert "Not Found" in res_get_author_byid.text
           break

# put author id
def test_put_author_id(Api_Author, My_New_Author):
    mylogger.info("test for put author by id")
    res = Api_Author.get_authors()
    author_id = res.json()[0]["id"]
    My_Update_Author = UpdateAuthorDto("UpdateNameAuthor",float(res.json()[0]["homeLatitude"]),float(res.json()[0]["homeLongitude"]),author_id)
    res = Api_Author.put_author_byid(author_id,My_Update_Author)
    assert res.status_code == 204

def test_put_autor_id_invalid_id(Api_Author):
    mylogger.info("test for put author with invalid id")
    res_get_authors = Api_Author.get_authors()
    authors_id = Authors_id(res_get_authors)
    while True:
        num = random.randint(0, len(authors_id) + 1)
        if num not in authors_id:
            My_Update_Author = UpdateAuthorDto("UpdateAuthor", float(res_get_authors.json()[0]["homeLatitude"]),
                                               float(res_get_authors.json()[0]["homeLongitude"]), num)
            res = Api_Author.put_author_byid(num, My_Update_Author)
            assert "Not Found" in res.text
            break

def test_put_autor_id_empty_name(Api_Author):
    mylogger.info("test for put author with empty name")
    res = Api_Author.get_authors()
    author_id = res.json()[0]["id"]
    My_Update_Author = UpdateAuthorDto("",float(res.json()[0]["homeLatitude"]),float(res.json()[0]["homeLongitude"]),author_id)
    res = Api_Author.put_author_byid(author_id,My_Update_Author)
    assert  "The Name field is required." in res.text

# delete author by id
def test_delete_autor_byid(Api_Author):
    mylogger.info("test for delete author by id")
    res = Api_Author.get_authors()
    author_id = res.json()[0]["id"]
    res_delete_author = Api_Author.delete_authors_id(author_id)
    assert res_delete_author.status_code == 204
    res_get_author_id = Api_Author.get_author_id(author_id)
    assert "Not Found" in res_get_author_id.text

def test_delete_autor_byid_invalid_id(Api_Author):
    mylogger.info("test for delete author by invalid id")
    res_get_authors = Api_Author.get_authors()
    authors_id = Authors_id(res_get_authors)
    while True:
        num = random.randint(0, len(authors_id) + 1)
        if num not in authors_id:
            res = Api_Author.delete_authors_id(num)
            assert "Not Found" in res.text
            break

## get search
def test_get_autor_search(Api_Author):
    mylogger.info("test for get author by name search")
    res_get_authors = Api_Author.get_authors()
    authors_name = res_get_authors.json()[0]["name"]
    res_get_author_search = Api_Author.get_authors_search_txt(authors_name)
    assert authors_name in res_get_author_search.text

##################### BOOKS
#get books
def test_get_books(Api_Book):
    mylogger.info("test for get books")
    res_get_books = Api_Book.get_books()
    books_name = res_get_books.json()[0]["name"]
    assert books_name in res_get_books.text

#post book
def test_post_book(Api_Book,Api_Author):
    mylogger.info("test for post book")
    res_get_authors = Api_Author.get_authors()
    authors_id = res_get_authors.json()[0]["id"]
    New_book = My_New_Book(authors_id)
    res_post_book = Api_Book.post_book(New_book)
    assert res_post_book.json()["name"] == New_book.name

def test_post_book_empty_name(Api_Book,Api_Author):
    mylogger.info("test for post book with empty name")
    res_get_authors = Api_Author.get_authors()
    authors_id = res_get_authors.json()[0]["id"]
    New_book = My_New_Book(authors_id)
    New_book.name = ""
    res_post_book = Api_Book.post_book(New_book)
    assert "The Name field is required." in res_post_book.text

@pytest.mark.skip(reason="the response is allways 500")
def test_post_book_invalid_authorid(Api_Book,Api_Author):## 500
    mylogger.info("test for post book with invalid author id")
    res_get_authors = Api_Author.get_authors()
    authors_id = Authors_id(res_get_authors)
    while True:
        num = random.randint(0, len(authors_id) + 1)
        if num not in authors_id:
            New_book = My_New_Book(num)
            res_post_book = Api_Book.post_book(New_book)
            mylogger.info(res_post_book.text)
            assert "The authorId field is required." in res_post_book.text
            break

def test_post_book_error_authorid(Api_Book):
    mylogger.info("test for post book with error author id")
    booksApi = Api_Book
    My_book = My_New_Book(-7)
    res_post_book = booksApi.post_book(My_book)
    assert "The field AuthorId must be between 1 and 2147483647." in res_post_book.text

#GET - BOOK BY ID
def test_get_book_byid(Api_Book):
    mylogger.info("test for get book by id")
    res_get_books = Api_Book.get_books()
    book_id = res_get_books.json()[0]["id"]
    res_get_book_byid = Api_Book.get_book_byid(book_id)
    assert res_get_books.json()[0]["name"] in res_get_book_byid.text

def test_get_book_invalid_byid(Api_Book):
    mylogger.info("test for get book with invalid id")
    res_get_books = Api_Book.get_books()
    book_id = Books_id(res_get_books)
    while True:
        num = random.randint(0, len(book_id) + 1)
        if num not in book_id:
            res = Api_Book.get_book_byid(num)
            assert "Not Found" in res.text
            break

#PUT - BOOK BY ID:
def test_put_book_byid(Api_Book,Api_Author):
    mylogger.info("test for put book by id")
    res_get_books = Api_Book.get_books()
    New_book = BookDto("UpDateNameBook", res_get_books.json()[0]["description"],
                               int(res_get_books.json()[0]["price"]), int(res_get_books.json()[0]["amountInStock"]),
                               res_get_books.json()[0]["imageUrl"], res_get_books.json()[0]["authorId"],res_get_books.json()[0]["id"])
    res_put_book_id = Api_Book.put_book_byid(res_get_books.json()[0]["id"], New_book)
    assert res_put_book_id.status_code == 204

def test_put_book_by_invalid_book_id(Api_Book, Api_Author):
    mylogger.info("test for put book by invalid book id")
    res_get_books = Api_Book.get_books()
    books_id = Books_id(res_get_books)
    while True:
        num = random.randint(0, len(books_id) + 1)
        if num not in books_id:
            New_book = BookDto(res_get_books.json()[0]["name"],res_get_books.json()[0]["description"],
                               int(res_get_books.json()[0]["price"]),int(res_get_books.json()[0]["amountInStock"]),
                               res_get_books.json()[0]["imageUrl"],res_get_books.json()[0]["authorId"],num)
            res_put_book_id = Api_Book.put_book_byid(num,New_book)
            assert "Not Found" in res_put_book_id.text
            break


def test_put_book_byid_empty_name(Api_Book):
    mylogger.info("test for put book by empty book name")
    res_get_books = Api_Book.get_books()
    New_book = BookDto("", res_get_books.json()[0]["description"],
                       int(res_get_books.json()[0]["price"]), int(res_get_books.json()[0]["amountInStock"]),
                       res_get_books.json()[0]["imageUrl"], res_get_books.json()[0]["authorId"],
                       res_get_books.json()[0]["id"])
    res_put_book_id = Api_Book.put_book_byid(res_get_books.json()[0]["id"], New_book)
    assert "The Name field is required." in res_put_book_id.text

def test_put_book_by_invalid_authorId(Api_Book,Api_Author):
    mylogger.info("test for put book by invalid author id")
    res_get_books = Api_Book.get_books()
    res_get_authors = Api_Author.get_authors()
    author_id = Authors_id(res_get_authors)
    while True:
        invalid_author_id = random.randint(0, len(author_id) + 1)
        if invalid_author_id not in author_id:
            New_book = BookDto(res_get_books.json()[0]["name"], res_get_books.json()[0]["description"],
                               int(res_get_books.json()[0]["price"]), int(res_get_books.json()[0]["amountInStock"]),
                               res_get_books.json()[0]["imageUrl"], res_get_books.json()[0]["authorId"], invalid_author_id)
            res_put_book_id = Api_Book.put_book_byid(invalid_author_id, New_book)
            assert "Not Found" in res_put_book_id.text
            break



# DELETE BOOK BY ID BUG
@pytest.mark.skip(reason="BUG")
def test_delete_book_byid(Api_Book):#######BUG 403
    mylogger.info("test for delete book by id")
    res_get_books = Api_Book.get_books()
    book_id = res_get_books.json()[0]["id"]
    res_delete_book =Api_Book.delete_book_byid(book_id)
    assert res_delete_book.status_code == 200

@pytest.mark.skip(reason="BUG")
def test_delete_book_by_invalid_id(Api_Book):#######BUG 403
    mylogger.info("test for delete book with invalid id")
    id_book = -9
    res_delete_book =Api_Book.delete_book_byid(id_book)
    assert "Not Found" in res_delete_book.text

#GET BOOK BY AUTHOR ID
def test_get_books_by_authorid(Api_Author, Api_Book):
    mylogger.info("test for get books by author id")
    res_get_author_id = Api_Author.get_authors()
    res_authors_id = Authors_id(res_get_author_id)
    author_id = res_authors_id[0]
    res = Api_Book.get_books_by_author_id(author_id)
    for book in res.json():
        assert book["authorId"] == author_id

def test_get_books_by_invalid_authorid(Api_Book,Api_Author):
    mylogger.info("test for get book by invalid author id")
    res_get_authors = Api_Author.get_authors()
    authors_id = Authors_id(res_get_authors)
    while True:
        num = random.randint(0, len(authors_id) + 1)
        if num not in authors_id:
            res = Api_Book.get_books_by_author_id(num)
            assert len(res.json()) == 0
            break

#PUT BOOK PURCHASE ID
def test_put_book_purchase_byid(Api_Book):
    mylogger.info("test for put book purchase by id")
    res_get_books_id = Api_Book.get_books()
    book_id = Books_id(res_get_books_id)
    res = Api_Book.put_book_purchase_byid(book_id[0])
    assert res_get_books_id.json()[0]["name"] in res.text

def test_put_book_purchase_by_invalid_id(Api_Book):
    mylogger.info("test for put book purchase by invalid id")
    res_get_books_id = Api_Book.get_books()
    book_id = Books_id(res_get_books_id)
    while True:
        num = random.randint(0, len(book_id)+1)
        if num not in book_id:
            res = Api_Book.put_book_purchase_byid(num)
            assert "400 Bad Request - purchase unsucessful" in res.text
            break