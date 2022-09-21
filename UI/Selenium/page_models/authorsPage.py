from UI.Selenium.page_models.basicPage import BasicPage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import re


class AuthorsPage(BasicPage):
    def __init__(self, driver):
        super().__init__(driver)

    def authors_of_the_store(self):
        """
        A function that return all the authors who have a book in the store
        """
        return self._driver.find_elements(*self.locator_dictionary["author_card"])

    def to_author_page(self, num):
        """
        A function that go to some author page
        :param num: author number
        """
        if not isinstance(num, int):
            raise TypeError("num parameter must be a integer")
        self.authors_of_the_store()[num].find_element(*self.locator_dictionary["to_author_page_button"]).click()
        return self._driver

    def author_name(self, num):
        """
        A function that return a name of some author
        """
        return self.authors_of_the_store()[num].find_element(*self.locator_dictionary["author_name"]).text
