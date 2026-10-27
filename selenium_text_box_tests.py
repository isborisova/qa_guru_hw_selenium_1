import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
        self.wait = WebDriverWait(self.driver, 5)
        yield
        self.driver.quit()

    def full_name_field(self, full_name):
        self.driver.find_element(*self.FULL_NAME_FIELD).send_keys(full_name)

    def email_field(self, email):
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def current_address_field(self, current_address):
        self.driver.find_element(*self.CURRENT_ADDRESS_FIELD).send_keys(current_address)

    def permanent_address_field(self, permanent_address):
            self.driver.find_element(*self.PERMANENT_ADDRESS_FIELD).send_keys(permanent_address)

    # Здесь у меня маленький экран и нужна прокрутка, пришлось спрашивать у DeepSeek
    def submit_button(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

    def result_box(self):
        return self.driver.find_element(*self.RESULT_BOX)

    def result_box_name(self):
        return self.driver.find_element(*self.RESULT_NAME).text

    def result_box_email(self):
        return self.driver.find_element(*self.RESULT_EMAIL).text

    def result_current_address(self):
        return self.driver.find_element(*self.RESULT_CURRENT_ADDRESS).text

    def result_permanent_address(self):
        return self.driver.find_element(*self.RESULT_PERMANENT_ADDRESS).text


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
        "example@com", "ivanexample.com", ""
    ])
    def test_invalid_email(self, setup, email):
        self.email_field(email)
        self.submit_button()
        result_box = self.driver.find_elements(*self.RESULT_BOX)
        assert len(result_box) == 1
        print("Блок результатов не показан при невалидном email")