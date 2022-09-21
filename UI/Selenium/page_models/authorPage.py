from UI.Selenium.page_models.basicPage import BasicPage


class AuthorPage(BasicPage):
    def __init__(self, driver):
        super().__init__(driver)

    def author_name(self):
        """
        A function that return the author name
        """
        return self._driver.find_element(*self.locator_dictionary["author_name_title"]).text

    def author_books(self):
        """
        A function that return all the author's book
        """
        return self._driver.find_elements(*self.locator_dictionary["author_book"])
