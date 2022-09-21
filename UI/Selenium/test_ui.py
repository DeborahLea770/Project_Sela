import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from UI.Selenium.page_models.loginPage import LoginPage
from UI.Selenium.page_models.storePage import StorePage
from UI.Selenium.page_models.registerPage import RegisterPage
from UI.Selenium.page_models.basicPage import BasicPage
from UI.Selenium.page_models.authorsPage import AuthorsPage
from UI.Selenium.page_models.authorPage import AuthorPage
from UI.Selenium.page_models.searchPage import SearchPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
from selenium.webdriver.common.by import By
import logging
from UI.conftest import package_name

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()
chrom_driver_path = package_name


def enter_main_page(url) -> BasicPage:
    """
    A function that go to main page
    """
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    return BasicPage(driver)


def enter_store_page(page):
    """
    A function that go to store page
    """
    return StorePage(page.click_store_link())


def open_login_page_and_submit(url, email: str, password: str):
    """
    A function that enter login page and submit the login form by two inputs which sent as parameters
    :param email: str, email input
    :param password: str, password input
    """
    main_page = enter_main_page(url)
    login_page = LoginPage(main_page.driver)
    login_page.fill_email_input(email)
    login_page.fill_password_input(password)
    next_page = StorePage(login_page.click_sign_in())
    time.sleep(2)
    return next_page


def open_register_page_and_submit(url, email: str, password: str, firstname: str, lastname: str):
    """
    A function that enter to register page and submit the register form
    by register inputs which sent as parameters
    """
    main_page = enter_main_page(url)
    login_page = LoginPage(main_page.driver)
    register_page = RegisterPage(login_page.click_register_button())
    register_page.fill_email_input(email)
    register_page.fill_password_input(password)
    register_page.fill_firstname_input(firstname)
    register_page.fill_lastname_input(lastname)
    register_page.click_sign_up()
    return register_page


def enter_authors_page(page):
    """
    A function that go to authors page
    """
    return AuthorsPage(page.click_authors_link())


def enter_search_page(page, text):
    """
    A function that go to search page by clicking search button
    after filling the search input with some text
    :param text: str, A text to fill the search input
    """
    page.fill_search_input(text)
    page.click_search_button()
    return SearchPage(page.click_search_button())


def test_links(url):
    mylogger.info("test for the main links")
    main_page = enter_main_page(url)
    store_page = StorePage(main_page.click_store_link())
    assert store_page.url() == "http://localhost/store"
    authors_page = AuthorsPage(main_page.click_authors_link())
    assert authors_page.url() == "http://localhost/authors"
    login_page = LoginPage(main_page.click_login_link())
    assert login_page.url() == "http://localhost/"
    main_page.close_page()


def test_register_empty_email(url, unregister_user):
    mylogger.info("test for register with empty email input")
    register_page = open_register_page_and_submit(url, "", unregister_user["password"], "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_invalid_email(url, unregister_user):
    mylogger.info("test for register with invalid email input")
    register_page = open_register_page_and_submit(url, "admin@", unregister_user["password"], "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_shorter_password(url, unregister_user):
    mylogger.info("test for register with password input shorter than allowed")
    register_page = open_register_page_and_submit(url, unregister_user["email"], "123", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_longer_password(url, unregister_user):
    mylogger.info("test for register with password input longer than allowed")
    register_page = open_register_page_and_submit(url, unregister_user["email"], "12345678910111213", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_empty_password(url, unregister_user):
    mylogger.info("test for register with empty password input")
    register_page = open_register_page_and_submit(url, unregister_user["email"], "", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_empty_firstname(url, unregister_user):
    mylogger.info("test for register with empty firstname input")
    register_page = open_register_page_and_submit(url, unregister_user["email"], unregister_user["password"], "", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_empty_lastname(url, unregister_user):
    mylogger.info("test for register with empty lastname input")
    register_page = open_register_page_and_submit(url, unregister_user["email"], unregister_user["password"], "deborah", "")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


def test_register_registered_email(url, register_user):
    mylogger.info("test for register with registered user")
    register_page = open_register_page_and_submit(url, register_user["email"], "24531", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"
    register_page.close_page()


@pytest.mark.skip(reason="No details about what happen after valid registration")
def test_register_valid(url, unregister_user):
    mylogger.info("test for valid registration")
    register_page = open_register_page_and_submit(url, unregister_user["email"], unregister_user["password"], "deborah", "fellous")
    assert register_page.url() == "http://localhost/store"
    register_page.close_page()


def test_login_empty_email(url, register_user):
    mylogger.info("test for login with empty email input")
    next_page = open_login_page_and_submit(url, "", register_user["password"])
    assert next_page.url() == "http://localhost/"
    next_page.close_page()


def test_login_invalid_email(url, register_user):
    mylogger.info("test for login with invalid email input")
    next_page = open_login_page_and_submit(url, "admin@", register_user["password"])
    assert next_page.url() == "http://localhost/"
    next_page.close_page()


def test_login_empty_password(url, register_user):
    mylogger.info("test for login with empty password input")
    next_page = open_login_page_and_submit(url, register_user["email"], "")
    assert next_page.url() == "http://localhost/"
    next_page.close_page()


def test_login_unregistered_user(url, unregister_user):
    mylogger.info("test for login with unregistered user")
    next_page = open_login_page_and_submit(url, unregister_user["email"], unregister_user["password"])
    assert next_page.url() == "http://localhost/"
    next_page.close_page()


def test_login_registered_user(url, register_user):
    mylogger.info("test for login with registered user")
    next_page = open_login_page_and_submit(url, register_user["email"], register_user["password"])
    assert next_page.url() == "http://localhost/store"
    next_page.close_page()


def test_buy_book_without_login(url, register_user):
    mylogger.info("test for buy book without login")
    main_page = enter_main_page(url)
    store_page = enter_store_page(main_page)
    books = store_page.books_of_the_store()
    store_page.buy_book(random.randint(0, len(books)-1))
    assert "Must be signed in to purchase" in store_page.message_after_purchase()
    store_page.close_page()


# def test_buy_book_with_login(url, register_user):
#     mylogger.info("test for buy book with login")
#     store_page = open_login_page_and_submit(url, register_user["email"], register_user["password"])
#     books = store_page.books_of_the_store()
#     time.sleep(3)
#     for num in range(len(books)):
#         if store_page.book_amount(num) > 0:
#             starting_amount = store_page.book_amount(num)
#             store_page.buy_book(num)
#             mylogger.info(num)
#             assert "Thank you for your purchase" in store_page.message_after_purchase()
#             store_page.driver.refresh()
#             assert starting_amount - 1 == store_page.book_amount(num)
#             store_page.close_page()
#             break
#
def test_buy_book_zero_amount(url, register_user):
    mylogger.info("test for buy book with 0 amount")
    store_page = open_login_page_and_submit(url, register_user["email"], register_user["password"])
    books = store_page.books_of_the_store()
    for num in range(len(books)):
        if store_page.book_amount(num) == 0:
            store_page.buy_book(num)
            store_page.message_after_purchase()
            time.sleep(2)
            assert "Request failed with status code 400" in store_page.message_after_purchase()
            store_page.close_page()
            break


def test_logout(url, register_user):
    mylogger.info("test for logout the user")
    store_page = open_login_page_and_submit(url, register_user["email"], register_user["password"])
    store_page.click_logout_button()
    books = store_page.books_of_the_store()
    store_page.buy_book(random.randint(0, len(books)-1))
    assert "Must be signed in to purchase" in store_page.message_after_purchase()
    store_page.close_page()


def test_link_to_author_page(url):
    mylogger.info("test for enter to some author page from store page")
    main_page = enter_main_page(url)
    authors_page = enter_authors_page(main_page)
    authors = authors_page.authors_of_the_store()
    author = random.randint(0, len(authors)-1)
    author_name = authors_page.author_name(author)
    author_page = AuthorPage(authors_page.to_author_page(author))
    assert author_name == author_page.author_name()
    author_page.close_page()


def test_books_of_author_in_author_page(url):
    mylogger.info("test for books in some author page")
    main_page = enter_main_page(url)
    authors_page = enter_authors_page(main_page)
    authors = authors_page.authors_of_the_store()
    author = random.randint(0, len(authors)-1)
    author_page = AuthorPage(authors_page.to_author_page(author))
    WebDriverWait(author_page.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "book-container")))
    books = author_page.author_books()
    for book in books:
        assert author_page.author_name() in book.text
    author_page.close_page()


def test_valid_amount_author_books(url):
    mylogger.info("test for valid amount of books in some author page")
    main_page = enter_main_page(url)
    authors_page = enter_authors_page(main_page)
    authors = authors_page.authors_of_the_store()
    author = random.randint(0, len(authors)-1)
    author_page = AuthorPage(authors_page.to_author_page(author))
    author_name = author_page.author_name()
    author_books = author_page.author_books()
    store_page = enter_store_page(author_page)
    filtered = filter(lambda book: author_name in book.text, store_page.books_of_the_store())
    assert len(author_books) == len(list(filtered))
    store_page.close_page()


def test_empty_search_input(url):
    mylogger.info("test for search with empty search input")
    main_page = enter_main_page(url)
    search_page = enter_search_page(main_page, "")
    WebDriverWait(search_page.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "card-group")))
    search_results = search_page.search_results()
    authors = AuthorsPage(search_page.click_authors_link()).authors_of_the_store()
    books = StorePage(search_page.click_store_link()).books_of_the_store()
    assert len(search_results) == len(books) + len(authors)
    search_page.close_page()


def test_book_search(url):
    mylogger.info("test for search for some book")
    main_page = enter_main_page(url)
    store_page = enter_store_page(main_page)
    books = store_page.books_of_the_store()
    book = random.randint(0, len(books)-1)
    book_name = store_page.book_name(book)
    search_page = enter_search_page(store_page, book_name)
    search_results = search_page.search_results()
    assert len(search_results) < len(books)
    for result in search_results:
        assert book_name in result.text
    search_page.close_page()


def test_author_search(url):
    mylogger.info("test for search for some author")
    main_page = enter_main_page(url)
    authors_page = enter_authors_page(main_page)
    authors = authors_page.authors_of_the_store()
    author = random.randint(0, len(authors) - 1)
    book_name = authors_page.author_name(author)
    search_page = enter_search_page(authors_page, book_name)
    search_results = search_page.search_results()
    assert len(search_results) < len(authors)
    for result in search_results:
        assert book_name in result.text
    search_page.close_page()

def test_fake_book_search(url):
    mylogger.info("test for search for some book that not exists in the system")
    main_page = enter_main_page(url)
    store_page = StorePage(main_page.click_store_link())
    books = store_page.books_of_the_store()
    WebDriverWait(main_page.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "book-container")))
    books_names = []
    for index in range(len(books)):
        books_names.append(store_page.book_name(index))
    book_name = string.ascii_letters
    if book_name not in books_names:
        search_page = enter_search_page(store_page, book_name)
        search_results = search_page.search_results()
        assert len(search_results) == 0
        search_page.close_page()


def test_fake_author_search(url):
    mylogger.info("test for search for some author that not exists in the system")
    main_page = enter_main_page(url)
    authors_page = enter_authors_page(main_page)
    authors = authors_page.authors_of_the_store()
    WebDriverWait(authors_page.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "author-container")))
    authors_names = []
    for index in range(len(authors)):
        authors_names.append(authors_page.author_name(index))
    author_name = string.ascii_letters
    if author_name not in authors_names:
        search_page = enter_search_page(authors_page, author_name)
        search_results = search_page.search_results()
        assert len(search_results) == 0
        search_page.close_page()
