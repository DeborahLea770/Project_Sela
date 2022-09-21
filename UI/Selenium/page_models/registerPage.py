from UI.Selenium.page_models.basicPage import BasicPage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import re


class RegisterPage(BasicPage):
    def __init__(self, driver):
        super().__init__(driver)
    locator_dictionary = {
      "sign_up_button": (By.CSS_SELECTOR, ".container-sm > form > button"),
      "password_input": (By.ID, 'password'),
      "email_input": (By.ID, 'email'),
      "firstname_input": (By.ID, 'firstName'),
      "lastname_input": (By.ID, 'lastName')
    }

    def click_sign_up(self):
        """
        A function that submit login form
        """
        self._driver.find_element(*self.locator_dictionary["sign_up_button"]).click()
        return self._driver

    def fill_password_input(self, text: str):
        """
        A function that fill the password input with a text
        :param text: str
        """
        self._driver.find_element(*self.locator_dictionary["password_input"]).send_keys(text)

    def fill_email_input(self, text: str):
        """
        A function that fill the email input with a text
        :param text: str
        """
        self._driver.find_element(*self.locator_dictionary["email_input"]).send_keys(text)

    def fill_firstname_input(self, text: str):
        """
        A function that fill the firstname input with a text
        :param text: str
        """
        self._driver.find_element(*self.locator_dictionary["firstname_input"]).send_keys(text)

    def fill_lastname_input(self, text: str):
        """
        A function that fill the lastname input with a text
        :param text: str
        """
        self._driver.find_element(*self.locator_dictionary["lastname_input"]).send_keys(text)
