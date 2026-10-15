import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. Запуск браузера Chrome
driver = webdriver.Chrome()

try:
    # 2. Открытие страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)  # Пауза, чтобы визуально заметить открытие

    # 3. Поиск элементов и заполнение полей
    # Находим поле currentAddress по его ID и вводим текст
    full_name_field = driver.find_element(By.ID, "currentAddress")
    #web_elements = driver.find_elements(By.XPATH, "someXPath")

    full_name_field.send_keys("Улица Матроскина, дом 99, квартира 33")

    # Находим кнопку Submit по ее ID и кликаем
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    # 4. Проверка результата
    time.sleep(5)  # Пауза, чтобы увидеть результат отправки

    # Находим блок с отправленными данными
    result_box = driver.find_element(By.ID, "output")

    # Проверяем, что в блоке результата появился введенный текст
    assert "Улица Матроскина, дом 99, квартира 33" in result_box.text
    print("Тест успешно пройден!")

finally:
    # 5. Закрытие браузера в любом случае
    driver.quit()