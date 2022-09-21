import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class BasicPage:
    def __init__(self, driver: webdriver):
        self._driver = driver

    locator_dictionary = {
      "body": (By.TAG_NAME, 'body'),
      "store_link": (By.XPATH, "//a[@href='/store']"),
      "authors_link": (By.XPATH, "//a[@href='/authors']"),
      "login_link": (By.XPATH, "//a[@href='/']"),
      "logout_button": (By.CSS_SELECTOR, ".navbar-nav > button"),
      "search_input": (By.ID, "searchtext"),
      "search_button": (By.XPATH, "//*/nav/div/form/button"),
      "book_card": (By.CLASS_NAME, "book-container"),
      "purchase_button": (By.CSS_SELECTOR, "div.card-footer > button"),
      "book_amount": (By.XPATH, "//*[text()='Left In Stock']]"),
      "book_name": (By.CSS_SELECTOR, ".card-body > .card-title"),
      "author_card": (By.CLASS_NAME, "author-container"),
      "to_author_page_button": (By.CSS_SELECTOR, "div.card-footer > button"),
      "author_name": (By.CSS_SELECTOR, ".card-body > .card-title"),
      "author_name_title": (By.CSS_SELECTOR, "h1 > .badge"),
      "author_book": (By.CLASS_NAME, "book-container"),
      "authors_search_results": (By.CLASS_NAME, "author-container"),
      "books_search_results": (By.CLASS_NAME, "book-container")
    }

    # root > nav > div > div > button
    @property
    def driver(self):
        """Gets the driver of this Model.
        :return: The driver of this Model.
        """
        return self._driver

    def text(self) -> str:
        """
        A function that return all the text inside the page
        :return: str
        """
        return self._driver.find_element(By.TAG_NAME, 'body').text

    def text_is_inside(self, text: str) -> bool:
        """
        A function that check if the text is inside the page or not
        :param text: str
        :return: True if the text is inside the page, False if not
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string!")
        return text in self.text()

    def url(self):
        """
        A function that return the url of the page
        :return:
        """
        return self._driver.current_url

    def click_store_link(self):
        """
        A function that click on the link for store page on the navbar
        """
        self._driver.find_element(*self.locator_dictionary["store_link"]).click()
        return self._driver

    def click_authors_link(self):
        """
        A function that click on the link for authors page on the navbar
        """
        self._driver.find_element(*self.locator_dictionary["authors_link"]).click()
        return self._driver

    def click_login_link(self):
        """
        A function that click on the link for login page on the navbar
        """
        self._driver.find_element(*self.locator_dictionary["login_link"]).click()
        return self._driver

    def click_logout_button(self):
        """
        A function that click on the logout button on navbar
        """
        self._driver.find_element(*self.locator_dictionary["logout_button"]).click()

    def fill_search_input(self, text: str):
        """
        A function that fill search input on the navbar with some text
        :param text: str, A text to fill the search input
        """
        if not isinstance(text, str):
            raise TypeError("text parameter must be a string!")
        self._driver.find_element(*self.locator_dictionary["search_input"]).send_keys(text)

    def click_search_button(self):
        """
        A function that click on search button on the navbar
        """
        self._driver.find_element(*self.locator_dictionary["search_button"]).click()
        return self._driver

    def close_page(self):
        """
        A function that close the page
        """
        self._driver.close()
