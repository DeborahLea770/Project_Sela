import time

from UI.Playwright.page_models.basicPage import BasicPage


class StorePage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

    def books_of_the_store(self):
        """
        A function that return all the books in the store
        """
        return self._page.locator(self.locator_dictionary["book_card"])

    def buy_book(self, num: int):
        """
        A function that choose some book from the store by num parameter and purchase it
        :param num: int
        """
        if not isinstance(num, int):
            raise TypeError("num parameter must be a integer")
        self.books_of_the_store().nth(num).locator(self.locator_dictionary["purchase_button"]).click()

    def book_amount(self, num: int) -> int:
        """
        A function that return the amount of books that left in the store
        :parma num: int, the index of book in the store
        """
        book_details = self.books_of_the_store().nth(num).inner_text()
        book_details_filter = book_details.replace('Purchase', '')
        return int(book_details_filter[-1])

    def book_name(self, num) -> int:
        """
        A function that return a name of some author
        :parma num: int, the index of book in the store
        """
        return self.books_of_the_store().nth(num).locator(self.locator_dictionary["book_name"]).inner_text()
