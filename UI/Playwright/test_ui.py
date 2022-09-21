import time
import pytest
from _pytest.fixtures import pytestconfig

import UI.conftest
from UI.Playwright.page_models.loginPage import LoginPage
from UI.Playwright.page_models.storePage import StorePage
from UI.Playwright.page_models.registerPage import RegisterPage
from UI.Playwright.page_models.basicPage import BasicPage
from UI.Playwright.page_models.authorsPage import AuthorsPage
from UI.Playwright.page_models.authorPage import AuthorPage
from UI.Playwright.page_models.searchPage import SearchPage
from playwright.sync_api import sync_playwright
import re
import logging
from threading import Event
import random
import string
from playwright.sync_api import Dialog
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()
from UI.conftest import brow

def enter_main_page(playwright, url, brow) -> BasicPage:
    """
    A function that go to main page
    """
    if brow == "firefox":
       browser = playwright.firefox.launch(headless=False)
    else:
       browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.on('dialog', lambda dialog: dialog.accept())
    return BasicPage(page)

def enter_store_page(page):
    """
    A function that go to store page
    """
    return StorePage(page.click_store_link())


def open_login_page_and_submit(playwright, url,brow, email: str, password: str):
    """
    A function that enter login page and submit the login form by two inputs which sent as parameters
    :param email: str, email input
    :param password: str, password input
    """
    main_page = enter_main_page(playwright, url , brow)
    login_page = LoginPage(main_page.page)
    login_page.fill_email_input(email)
    login_page.fill_password_input(password)
    next_page = StorePage(login_page.click_sign_in())
    next_page.page.wait_for_timeout(2000)
    return next_page


def open_register_page_and_submit(url,brow, email: str, password: str, firstname: str, lastname: str):
    """
    A function that enter to register page and submit the register form
    by register inputs which sent as parameters
    """
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url, brow)
        login_page = LoginPage(main_page.page)
        register_page = RegisterPage(login_page.click_register_button())
        register_page.fill_email_input(email)
        register_page.fill_password_input(password)
        register_page.fill_firstname_input(firstname)
        register_page.fill_lastname_input(lastname)
        register_page.click_sign_up()
        register_page.page.wait_for_timeout(2000)
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


def message_after_purchase(dialog, text: str):
    """
    A function that check if some text is inside dialog box
    :param text:str, A text to check
    """
    if not isinstance(text, str):
        raise TypeError("text parameter must be a string!")
    assert text in dialog.message


def test_links(url , brow ):
    mylogger.info("test for the main links")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url , brow)
        store_page = StorePage(main_page.click_store_link())
        assert store_page.url() == "http://localhost/store"
        authors_page = AuthorsPage(main_page.click_authors_link())
        assert authors_page.url() == "http://localhost/authors"
        login_page = LoginPage(main_page.click_login_link())
        assert login_page.url() == "http://localhost/"

## REGISTER
def test_register_empty_email(url,brow,unregister_user):
    mylogger.info("test for register with empty email input")
    register_page = open_register_page_and_submit(url,brow, "", unregister_user["password"], "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"


def test_register_invalid_email(url,brow, unregister_user):
    mylogger.info("test for register with invalid email input")
    register_page = open_register_page_and_submit(url,brow, "admin@", unregister_user["password"], "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"


def test_register_shorter_password(url,brow, unregister_user):
    mylogger.info("test for register with password input shorter than allowed")
    register_page = open_register_page_and_submit(url,brow, unregister_user["email"], "123", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"


def test_register_longer_password(url,brow, unregister_user):
    mylogger.info("test for register with password input longer than allowed")
    register_page = open_register_page_and_submit(url,brow, unregister_user["email"], "12345678910111213", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"


def test_register_empty_password(url,brow, unregister_user):
    mylogger.info("test for register with empty password input")
    register_page = open_register_page_and_submit(url,brow, unregister_user["email"], "", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"


def test_register_empty_firstname(url,brow, unregister_user):
    mylogger.info("test for register with empty firstname input")
    register_page = open_register_page_and_submit(url,brow, unregister_user["email"], unregister_user["password"], "", "fellous")
    assert register_page.url() == "http://localhost/register"


def test_register_empty_lastname(url,brow, unregister_user):
    mylogger.info("test for register with empty lastname input")
    register_page = open_register_page_and_submit(url,brow, unregister_user["email"], unregister_user["password"], "deborah", "")
    assert register_page.url() == "http://localhost/register"


def test_register_registered_email(url,brow, register_user):
    mylogger.info("test for register with registered user")
    register_page = open_register_page_and_submit(url,brow, register_user["email"], "12345", "deborah", "fellous")
    assert register_page.url() == "http://localhost/register"


@pytest.mark.skip(reason="No details about what happen after valid registration")
def test_register_valid(url,brow, unregister_user):
    mylogger.info("test for valid registration")
    register_page = open_register_page_and_submit(url,brow, unregister_user["email"], unregister_user["password"], "deborah", "fellous")
    assert register_page.url() == "http://localhost/store"

###LOGIN

def test_login_empty_email(url,brow, register_user):
    mylogger.info("test for login with empty email input")
    with sync_playwright() as playwright:
        next_page = open_login_page_and_submit(playwright,url,brow, "", register_user["password"])
    assert next_page.url() == "http://localhost/"


def test_login_invalid_email(url,brow, register_user):
    mylogger.info("test for login with invalid email input")
    with sync_playwright() as playwright:
        next_page = open_login_page_and_submit(playwright,url,brow, "admin@", register_user["password"])
    assert next_page.url() == "http://localhost/"


def test_login_empty_password(url,brow, register_user):
    mylogger.info("test for login with empty password input")
    with sync_playwright() as playwright:
        next_page = open_login_page_and_submit(playwright,url,brow, register_user["email"], "")
    assert next_page.url() == "http://localhost/"


def test_login_unregistered_user(url,brow, unregister_user):
    mylogger.info("test for login with unregistered user")
    with sync_playwright() as playwright:
        next_page = open_login_page_and_submit(playwright,url,brow, unregister_user["email"], unregister_user["password"])
    assert next_page.url() == "http://localhost/"


def test_login_registered_user(url,brow, register_user):
    mylogger.info("test for login with registered user")
    with sync_playwright() as playwright:
        next_page = open_login_page_and_submit(playwright,url,brow, register_user["email"], register_user["password"])
    assert next_page.url() == "http://localhost/store"

#STORE BOOK
def test_buy_book_without_login(url,brow, register_user):
    mylogger.info("test for buy book without login")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        store_page = enter_store_page(main_page)
        store_page.page.wait_for_selector('.book-container')
        books = store_page.books_of_the_store()
        store_page.page.on('dialog', lambda dialog: message_after_purchase(dialog, "Must be signed in to purchase"))
        store_page.buy_book(random.randint(0, books.count()-1))


def test_buy_book_with_login(url,brow, register_user):
    mylogger.info("test for buy book with login")
    with sync_playwright() as playwright:
        store_page = open_login_page_and_submit(playwright, url,brow, register_user["email"], register_user["password"])
        books = store_page.books_of_the_store()
        for num in range(books.count()):
            if store_page.book_amount(num) > 0:
                store_page.page.on('dialog', lambda dialog: message_after_purchase(dialog, "Thank you for your purchase"))
                starting_amount = store_page.book_amount(num)
                store_page.buy_book(num)
                # # assert "Thank you for your purchase" in store_page.message_after_purchase()
                store_page.page.reload(timeout=0)
                time.sleep(4)
                assert starting_amount - 1 == store_page.book_amount(num)
                break


def test_buy_book_zero_amount(url,brow, register_user):
    mylogger.info("test for buy book with 0 amount")
    with sync_playwright() as playwright:
        store_page = open_login_page_and_submit(playwright, url,brow, register_user["email"], register_user["password"])
        books = store_page.books_of_the_store()
        for num in range(books.count()):
            if store_page.book_amount(num) == 0:
                store_page.page.on('dialog',
                                   lambda dialog: message_after_purchase(dialog, "Thank you for your purchase"))
                store_page.page.on('dialog',
                                   lambda dialog: message_after_purchase(dialog, "Request failed with status code 400"))
                store_page.buy_book(num)
                break


def test_logout(url,brow, register_user):
    mylogger.info("test for logout the user")
    with sync_playwright() as playwright:
        store_page = open_login_page_and_submit(playwright, url,brow, register_user["email"], register_user["password"])
        store_page.page.on('dialog', lambda dialog: message_after_purchase(dialog, "Must be signed in to purchase"))
        store_page.click_logout_button()
        books = store_page.books_of_the_store()
        store_page.buy_book(random.randint(0, books.count()-1))


def test_link_to_author_page(url,brow):
    mylogger.info("test for enter to some author page from store page")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        authors_page = enter_authors_page(main_page)
        authors = authors_page.authors_of_the_store()
        author = random.randint(0, authors.count()-1)
        author_name = authors_page.author_name(author)
        author_page = AuthorPage(authors_page.to_author_page(author))
        assert author_name == author_page.author_name()

###AUTHOR
def test_books_of_author_in_author_page(url,brow):
    mylogger.info("test for book in some author page")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        authors_page = enter_authors_page(main_page)
        authors = authors_page.authors_of_the_store()
        author = random.randint(0, authors.count()-1)
        author_page = AuthorPage(authors_page.to_author_page(author))
        author_page.page.wait_for_selector('.book-container')
        books = author_page.author_books()
        for book in books.all_inner_texts():
            assert author_page.author_name() in book


def test_valid_amount_author_books(url,brow):
    mylogger.info("test for valid amount of books in some author page")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        authors_page = enter_authors_page(main_page)
        authors = authors_page.authors_of_the_store()
        author = random.randint(0, authors.count() - 1)
        author_page = AuthorPage(authors_page.to_author_page(author))
        author_name = author_page.author_name()
        author_books = author_page.author_books().count()
        store_page = enter_store_page(author_page)
        filtered = filter(lambda book: author_name in book, store_page.books_of_the_store().all_inner_texts())
        assert author_books == len(list(filtered))

#SEARCH
def test_empty_search_input(url,brow):
    mylogger.info("test for search with empty search input")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        search_page = enter_search_page(main_page, "")
        search_page.page.wait_for_selector('.card-group')
        search_results = search_page.search_results()
        books = StorePage(search_page.click_store_link()).books_of_the_store().count()
        authors_and_books = books + AuthorsPage(search_page.click_authors_link()).authors_of_the_store().count()
        assert len(search_results) == authors_and_books


def test_book_search(url,brow):
    mylogger.info("test for search for some book")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        store_page = enter_store_page(main_page)
        books = store_page.books_of_the_store()
        book = random.randint(0, books.count()-1)
        book_name = store_page.book_name(book)
        search_page = enter_search_page(store_page, book_name)
        mylogger.info(books.count())
        search_results = search_page.search_results()
        assert len(search_results) < books.count()
        for result in search_results:
            assert book_name in result.inner_text()


def test_author_search(url,brow):
    mylogger.info("test for search for some author")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        authors_page = enter_authors_page(main_page)
        authors = authors_page.authors_of_the_store().count()
        author = random.randint(0, authors - 1)
        author_name = authors_page.author_name(author)
        search_page = enter_search_page(authors_page, author_name)
        search_results = search_page.search_results()
        assert len(search_results) < authors
        for result in search_results:
            assert author_name in result


def test_fake_book_search(url,brow):
    mylogger.info("test for search for some book that not exists in the system")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        store_page = StorePage(main_page.click_store_link())
        books = store_page.books_of_the_store()
        store_page.page.wait_for_selector('.book-container')
        books_names = []
        for index in range(books.count()):
            books_names.append(store_page.book_name(index))
        book_name = string.ascii_letters
        if book_name not in books_names:
            search_page = enter_search_page(store_page, book_name)
            search_results = search_page.search_results()
            assert len(search_results) == 0


def test_fake_author_search(url,brow):
    mylogger.info("test for search for some author that not exists in the system")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright, url,brow)
        authors_page = enter_authors_page(main_page)
        authors = authors_page.authors_of_the_store()
        authors_page.page.wait_for_selector('.author-container')
        authors_names = []
        for index in range(authors.count()):
            authors_names.append(authors_page.author_name(index))
        author_name = string.ascii_letters
        if author_name not in authors_names:
            search_page = enter_search_page(authors_page, author_name)
            search_results = search_page.search_results()
            assert len(search_results) == 0
