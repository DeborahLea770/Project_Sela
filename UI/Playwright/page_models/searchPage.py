from UI.Playwright.page_models.basicPage import BasicPage


class SearchPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

    def search_results(self):
        """
        A function that return all the search results
        """
        results = []
        authors = self._page.locator(self.locator_dictionary["authors_search_results"])
        books = self._page.locator(self.locator_dictionary["books_search_results"])
        results.extend(authors.all_inner_texts() + books.all_inner_texts())
        return results
