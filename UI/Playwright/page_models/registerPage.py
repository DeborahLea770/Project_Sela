from UI.Playwright.page_models.basicPage import BasicPage
from selenium.webdriver.common.by import By


class RegisterPage(BasicPage):
    def __init__(self, driver):
        super().__init__(driver)
    locator_dictionary = {
      "sign_up_button": 'button >> text=Submit',
      "password_input": '#password',
      "email_input": '#email',
      "firstname_input": '#firstName',
      "lastname_input": '#lastName'
    }

    def click_sign_up(self):
        """
        A function that submit login form
        """
        self._page.locator(self.locator_dictionary["sign_up_button"]).click()
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

    def fill_firstname_input(self, text: str):
        """
        A function that fill the firstname input with a text
        :param text: str
        """
        self._page.locator(self.locator_dictionary["firstname_input"]).fill(text)

    def fill_lastname_input(self, text: str):
        """
        A function that fill the lastname input with a text
        :param text: str
        """
        self._page.locator(self.locator_dictionary["lastname_input"]).fill(text)
