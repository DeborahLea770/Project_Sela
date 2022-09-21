from UI.Playwright.page_models.basicPage import BasicPage
from selenium.webdriver.common.by import By


class LoginPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)
    locator_dictionary = {
      "sign_in_button": 'button >> text=Submit',
      "password_input": '#password',
      "email_input": '#email',
      "register_button": 'button >> text=Register!'
    }

    def click_sign_in(self):
        """
        A function that submit login form
        """
        self._page.locator(self.locator_dictionary["sign_in_button"]).click()
        return self._page

    def fill_password_input(self, text: str):
        """
        A function that fill the password input with a text
        :param text: str
        """
        self._page.locator(self.locator_dictionary["password_input"]).fill(text)

    def fill_email_input(self, text: str):
        """
        A function that fill the email input with a text
        :param text: str
        """
        self._page.locator(self.locator_dictionary["email_input"]).fill(text)

    def click_register_button(self):
        """
        A function that click on register button and go to register page
        """
        self._page.locator(self.locator_dictionary["register_button"]).click()
        return self._page

