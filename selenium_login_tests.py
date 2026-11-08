import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec


class TestLoginForm:
    URL = "https://qa-guru.github.io/one-page-form/login.html"

    LOGIN_FIELD = (By.ID, "login-input")
    PASSWORD_FIELD = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "submit-button")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    WELCOME_MESSAGE = (By.ID, "welcome-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    @pytest.fixture(scope="function")
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(
            self.driver,
            timeout=5,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )
        yield
        self.driver.quit()

    # баловство, но я честно его скопипастила
    def field_login(self, login):
        element = self.wait.until(ec.visibility_of_element_located(self.LOGIN_FIELD))
        actions = ActionChains(self.driver)
        actions.click(element)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
        actions.send_keys(Keys.BACKSPACE)
        actions.send_keys(login)
        actions.send_keys(Keys.TAB)
        actions.perform()

    def field_password(self, password):
        element = self.wait.until(ec.visibility_of_element_located(self.PASSWORD_FIELD))
        actions = ActionChains(self.driver)
        actions.click(element)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
        actions.send_keys(Keys.BACKSPACE)
        actions.send_keys(password)
        actions.perform()

    def login_button(self):
        button = self.wait.until(ec.element_to_be_clickable(self.LOGIN_BUTTON))
        button.click()

    def logout_button(self):
        button = self.wait.until(ec.element_to_be_clickable(self.LOGOUT_BUTTON))
        button.click()

    def welcome_message_text(self):
        return self.wait.until(ec.visibility_of_element_located(self.WELCOME_MESSAGE)).text

    def error_message_text(self):
        return self.wait.until(ec.visibility_of_element_located(self.ERROR_MESSAGE)).text

    @pytest.mark.parametrize("login, password, expected", [
        ("user1", "password1", f"Welcome, user1!")
    ])
    def test_valid_data_login(self, setup, login, password, expected): # <-- добавили setup
        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.welcome_message_text() == expected

    @pytest.mark.parametrize("login, password, expected", [
        ("biba", "password1", "Wrong login or password"),
        ("user1", "bobaba", "Wrong login or password"),
    ])
    def test_invalid_login(self, setup, login, password, expected): # <-- добавили setup
        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.error_message_text() == expected

    def test_empty_fields(self, setup): # <-- добавили setup
        self.login_button()
        assert self.error_message_text() == "Login and password are required (minimum 3 and 6 characters)"


    def test_invalid_password(self, setup): # <-- добавили setup
        login = "user1"
        password = "password"

        self.field_login(login)
        self.field_password(password)
        self.login_button()

        assert self.error_message_text() == "Wrong login or password"

    def test_min_length(self, setup): # Проверяем, что отрабатывают граничные значения для 3 и 6 символов
        login = "bib"
        password = "bibibi"

        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.error_message_text() == "Wrong login or password"

    def test_less_min_login(self, setup): # Проверяем, что отрабатывают граничные значения для 2 и 5 символов
        login = "bi"
        password = "bibib"

        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.error_message_text() == "Login must be at least 3 characters"

    def test_less_min_pass(self, setup): # Проверяем, что отрабатывают граничные значения для 2 и 5 символов
        login = "bib"
        password = "bibib"

        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.error_message_text() == "Password must be at least 6 characters"

    def test_empty_pass(self, setup): # Проверяем, что отрабатывают граничные значения для 2 и 5 символов
        login = "bib"
        password = ""

        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.error_message_text() == "Password is required (minimum 6 characters)"
