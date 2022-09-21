from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from UI.Selenium.page_models.basicPage import BasicPage


class SearchPage(BasicPage):
    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def search_results(self):
        """
        A function that return all the search results
        """
        results = []
        authors = self._driver.find_elements(*self.locator_dictionary["authors_search_results"])
        books = self._driver.find_elements(*self.locator_dictionary["books_search_results"])
        results.extend(authors + books)
        return results
