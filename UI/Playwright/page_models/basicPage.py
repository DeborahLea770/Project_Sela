class BasicPage:
    def __init__(self, page):
        self._page = page

    locator_dictionary = {
      "store_link": '.nav-link >> text=Store',
      "authors_link": '.nav-link >> text=Authors',
      "login_link": '.nav-link >> text=Log In',
      "logout_button": '.navbar-nav >> text=Log Out',
      "search_input": '#searchtext',
      "search_button": 'button >> text=Search',
      "book_card": '.store-container >> .book-container',
      "purchase_button": 'div.card-footer >> button',
      # "book_amount": (By.XPATH, "//*[text()='Left In Stock']]"),
      "book_name": '.card-body >> .card-title',
      "author_card": '.author-container',
      "to_author_page_button": 'div.card-footer >> button',
      "author_name": '.card-body >> .card-title',
      "author_name_title": 'h1 >> .badge',
      "author_book": '.book-container',
      "authors_search_results": '.author-container',
      "books_search_results": '.book-container'
    }

    # root > nav > div > div > button
    @property
    def page(self):
        """Gets the driver of this Model.
        :return: The driver of this Model.
        """
        return self._page

    def text(self) -> str:
        """
        A function that return all the text inside the page
        :return: str
        """
        return self._page.locator('body').inner_html()

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
        return self._page.url

    def click_store_link(self):
        """
        A function that click on the link for store page on the navbar
        """
        self._page.locator(self.locator_dictionary["store_link"]).click()
        return self._page

    def click_authors_link(self):
        """
        A function that click on the link for authors page on the navbar
        """
        self._page.locator(self.locator_dictionary["authors_link"]).click()
        return self._page

    def click_login_link(self):
        """
        A function that click on the link for login page on the navbar
        """
        self._page.locator(self.locator_dictionary["login_link"]).click()
        return self._page

    def click_logout_button(self):
        """
        A function that click on the logout button on navbar
        """
        self._page.locator(self.locator_dictionary["logout_button"]).click()

    def fill_search_input(self, text: str):
        """
        A function that fill search input on the navbar with some text
        :param text: str, A text to fill the search input
        """
        if not isinstance(text, str):
            raise TypeError("text parameter must be a string!")
        self._page.locator(self.locator_dictionary["search_input"]).fill(text)

    def click_search_button(self):
        """
        A function that click on search button on the navbar
        """
        self._page.locator(self.locator_dictionary["search_button"]).click()
        return self._page

    def close_page(self):
        """
        A function that close the page
        """
        self._page.close()
