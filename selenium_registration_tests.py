import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec


class TestStudentRegistration:
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_MALE_LABEL = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
    MOBILE_NUMBER = (By.ID, "userNumber")
    DATE_INPUT = (By.ID, "dateOfBirthInput")
    MONTH_SELECT = (By.CLASS_NAME, "react-datepicker__month-select")
    YEAR_SELECT = (By.CLASS_NAME, "react-datepicker__year-select")
    DAY_ELEMENT = (By.CSS_SELECTOR, ".react-datepicker__day--002:not(.react-datepicker__day--outside-month)")
    SUBJECT_INPUT = (By.ID, "subjectsInput")
    UPLOAD_INPUT = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    STATE_DROPDOWN = (By.ID, "state")
    CITY_DROPDOWN = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")
    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")

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

    def close_banner(self):
        try:
            close_btn = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='fixedban']/div/div/button")))
            close_btn.click()
            self.wait.until(ec.invisibility_of_element(close_btn))
        except:
            pass

    def fill_first_name(self, name):
        el = self.wait.until(ec.visibility_of_element_located(self.FIRST_NAME))
        el.clear()
        el.send_keys(name)

    def fill_last_name(self, last_name):
        el = self.wait.until(ec.visibility_of_element_located(self.LAST_NAME))
        el.clear()
        el.send_keys(last_name)

    def fill_email(self, email):
        el = self.wait.until(ec.visibility_of_element_located(self.EMAIL))
        el.clear()
        el.send_keys(email)

    def select_gender_male(self):
        el = self.wait.until(ec.element_to_be_clickable(self.GENDER_MALE_LABEL))
        self.driver.execute_script("arguments[0].click();", el)

    def fill_mobile(self, mobile):
        el = self.wait.until(ec.visibility_of_element_located(self.MOBILE_NUMBER))
        el.clear()
        el.send_keys(mobile)

    def fill_date_of_birth(self):
        self.wait.until(ec.element_to_be_clickable(self.DATE_INPUT)).click()
        month = self.wait.until(ec.element_to_be_clickable(self.MONTH_SELECT))
        month.click()
        month.find_element(By.XPATH, "//option[@value='8']").click()
        year = self.wait.until(ec.element_to_be_clickable(self.YEAR_SELECT))
        year.click()
        year.find_element(By.XPATH, "//option[@value='1994']").click()
        self.wait.until(ec.element_to_be_clickable(self.DAY_ELEMENT)).click()

    def fill_subject(self, subject):
        el = self.wait.until(ec.visibility_of_element_located(self.SUBJECT_INPUT))
        el.send_keys(subject)
        el.send_keys(u'\ue007')

    def select_state(self, state_name):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")
        dropdown = self.wait.until(ec.element_to_be_clickable(self.STATE_DROPDOWN))
        dropdown.click()
        option = self.wait.until(ec.element_to_be_clickable((By.XPATH, f"//div[text()='{state_name}']")))
        option.click()

    def select_city(self, city_name):
        dropdown = self.wait.until(ec.element_to_be_clickable(self.CITY_DROPDOWN))
        dropdown.click()
        option = self.wait.until(ec.element_to_be_clickable((By.XPATH, f"//div[text()='{city_name}']")))
        option.click()

    def click_submit(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")
        btn = self.wait.until(ec.presence_of_element_located(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def test_full_registration(self, setup):
        self.close_banner()
        self.fill_first_name("Иван")
        self.fill_last_name("Иванов")
        self.fill_email("ivan.ivanov@example.com")
        self.select_gender_male()
        self.fill_mobile("79135757998")
        self.fill_date_of_birth()
        self.fill_subject("Tuda suda")
        address_field = self.wait.until(ec.visibility_of_element_located(self.CURRENT_ADDRESS_FIELD))
        address_field.send_keys("г. Пермь, ул Матроскина, д.11")
        self.select_state("NCR")
        self.select_city("Delhi")
        self.click_submit()

        modal = self.wait.until(ec.visibility_of_element_located(self.MODAL_TITLE))
        assert modal.text == "Thanks for submitting the form"
        print("Тест на заполнение формы PASS")

    def test_empty_required_fields(self, setup):
        self.close_banner()
        self.click_submit()

        try:
            self.wait.until(ec.invisibility_of_element_located(self.MODAL_TITLE))
            print("Тест на пустые поля PASS")
        except:
            assert False, "Заводите багулю"

    def test_only_first_name(self, setup):
        self.close_banner()
        self.fill_first_name("Иван")
        self.click_submit()

        try:
            self.wait.until(ec.invisibility_of_element_located(self.MODAL_TITLE))
            print("Тест на заполнение только имени PASS")
        except:
            assert False, "Заводите багулю"


    # На большее сил не хватило с ребенком, работой и обязанностями жены, извините