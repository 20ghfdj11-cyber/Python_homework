import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_calc():
    driver = webdriver.Chrome()  # Создаём драйвер вручную
    driver.maximize_window()
    try:
        url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        driver.get(url)
        delay_input = driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys("45")

        buttons = ["7", "+", "8", "="]
        for button in buttons:
            xpath = f"//span[text()='{button}']"
            driver.find_element(By.XPATH, xpath).click()

        result = WebDriverWait(driver, 45).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
        )

        assert result
    finally:
        driver.quit()