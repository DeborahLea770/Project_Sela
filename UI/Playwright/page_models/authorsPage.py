from UI.Playwright.page_models.basicPage import BasicPage


class AuthorsPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

    def authors_of_the_store(self):
        """
        A function that return all the authors who have a book in the store
        """
        return self._page.locator(self.locator_dictionary["author_card"])

    def to_author_page(self, num):
        """
        A function that go to some author page
        :param num: author number
        """
        if not isinstance(num, int):
            raise TypeError("num parameter must be a integer")
        self.authors_of_the_store().nth(num).locator(self.locator_dictionary["to_author_page_button"]).click()
        return self._page

    def author_name(self, num):
        """
        A function that return a name of some author
        """
        return self.authors_of_the_store().nth(num).locator(self.locator_dictionary["author_name"]).inner_text()
