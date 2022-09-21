from UI.Selenium.page_models.basicPage import BasicPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import re


class LoginPage(BasicPage):
    def __init__(self, driver):
        super().__init__(driver)
    locator_dictionary = {
      "sign_in_button": (By.CSS_SELECTOR, ".container-sm > form > button"),
      "password_input": (By.ID, 'password'),
      "email_input": (By.ID, 'email'),
      "register_button": (By.XPATH, "//*[text()='Register!']")
    }

    def click_sign_in(self):
        """
        A function that submit login form
        """
        self._driver.find_element(*self.locator_dictionary["sign_in_button"]).click()
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

    def click_register_button(self):
        """
        A function that click on register button and go to register page
        """
        self._driver.find_element(*self.locator_dictionary["register_button"]).click()
        return self._driver

