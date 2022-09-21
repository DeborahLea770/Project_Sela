from selenium import webdriver
from selenium.webdriver.common.by import By
from UI.Selenium.page_models.basicPage import BasicPage
from selenium.webdriver.common.keys import Keys


class StorePage(BasicPage):
    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def books_of_the_store(self):
        """
        A function that return all the books in the store
        """
        return self._driver.find_elements(*self.locator_dictionary["book_card"])

    def buy_book(self, num: int):
        """
        A function that choose some book from the store by num parameter and purchase it
        :param num: int
        """
        if not isinstance(num, int):
            raise TypeError("num parameter must be a integer")
        self.books_of_the_store()[num].find_element(*self.locator_dictionary["purchase_button"]).send_keys(Keys.ENTER)

    def message_after_purchase(self) -> str:
        """
        A function that return the text inside alert box after purchasing
        """
        alert = self._driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text

    def book_amount(self, num: int) -> int:
        """
        A function that return the amount of books that left in the store
        :parma num: int, the index of book in the store
        """
        book_details = self.books_of_the_store()[num].text
        book_details_filter = book_details.replace('Purchase', '')
        return int(book_details_filter[-1])

    def book_name(self, num) -> int:
        """
        A function that return a name of some book
        :parma num: int, the index of book in the store
        """
        return self.books_of_the_store()[num].find_element(*self.locator_dictionary["book_name"]).text

    def author_name(self):
        """
        A function that return the author name
        """
        return self._driver.find_element(*self.locator_dictionary["author_name_title"]).text
