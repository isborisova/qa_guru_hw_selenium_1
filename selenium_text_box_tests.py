import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

class TestTextBox:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"

    FULL_NAME_FIELD = (By.ID, "userName")
    EMAIL_FIELD = (By.ID, "userEmail")
    SUBMIT_BUTTON = (By.ID, "submit")
    RESULT_BOX = (By.ID, "output")
    PERMANENT_ADDRESS_FIELD = (By.ID, "permanentAddress")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    RESULT_NAME = (By.CSS_SELECTOR, "#output #name")
    RESULT_EMAIL = (By.CSS_SELECTOR, "#output #email")
    RESULT_CURRENT_ADDRESS = (By.CSS_SELECTOR, "#output #currentAddress")
    RESULT_PERMANENT_ADDRESS = (By.CSS_SELECTOR, "#output #permanentAddress")

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

    def full_name_field(self, full_name):
        element = self.wait.until(ec.visibility_of_element_located(self.FULL_NAME_FIELD))
        element.clear() # На всякий случай очищаем
        element.send_keys(full_name)

    def email_field(self, email):
        element = self.wait.until(ec.visibility_of_element_located(self.EMAIL_FIELD))
        element.clear()
        element.send_keys(email)

    def current_address_field(self, current_address):
        element = self.wait.until(ec.visibility_of_element_located(self.CURRENT_ADDRESS_FIELD))
        element.clear()
        element.send_keys(current_address)

    def permanent_address_field(self, permanent_address):
        element = self.wait.until(ec.visibility_of_element_located(self.PERMANENT_ADDRESS_FIELD))
        element.clear()
        element.send_keys(permanent_address)

    # Здесь с прокруточкой и сразу же кликом
    def submit_button(self):
        submit_button = self.wait.until(ec.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", submit_button)

    def result_box_name(self):
        return self.wait.until(ec.visibility_of_element_located(self.RESULT_NAME)).text

    def result_box_email(self):
        return self.wait.until(ec.visibility_of_element_located(self.RESULT_EMAIL)).text

    def result_current_address(self):
        return self.wait.until(ec.visibility_of_element_located(self.RESULT_CURRENT_ADDRESS)).text

    def result_permanent_address(self):
        return self.wait.until(ec.visibility_of_element_located(self.RESULT_PERMANENT_ADDRESS)).text


    @pytest.mark.parametrize("current_address", [
        "Улица Матроскина, дом 99, квартира 33"
    ])
    def test_valid_current_address(self, setup, current_address):
        self.current_address_field(current_address)
        self.submit_button()
        assert current_address in self.result_current_address()
        print("Тест на текущий адрес PASS")

    @pytest.mark.parametrize("permanent_address", [
        "Улица Шарика, дом 11, квартира 22"
    ])
    def test_valid_permanent_address(self, setup, permanent_address):
        self.permanent_address_field(permanent_address)
        self.submit_button()
        assert permanent_address in self.result_permanent_address()
        print("Тест на временный адрес PASS")

    @pytest.mark.parametrize("full_name", [
        "Ivan Ivanov"
    ])
    def test_valid_name(self, setup, full_name):
        self.full_name_field(full_name)
        self.submit_button()
        assert full_name in self.result_box_name()
        print("Тест на проверку имени PASS")

    @pytest.mark.parametrize("email", [
        "ivanexample.com",
        "example"
    ])
    def test_invalid_email(self, setup, email):
        self.email_field(email)
        self.submit_button()
        try:
            self.wait.until(ec.invisibility_of_element_located(self.RESULT_BOX))
            print("Тест с пустым email PASS")
        except:
            assert False

    def test_empty_email(self, setup):
        self.full_name_field("Boba Boooba")
        self.submit_button()
        result_box = self.wait.until(ec.visibility_of_element_located(self.RESULT_BOX))
        result_text = result_box.text
        assert "Email:\n" in result_text
        print("Тест с пустым email PASS")