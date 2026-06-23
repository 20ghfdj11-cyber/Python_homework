from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def test_dynamic_loading():
    driver = webdriver.Chrome()

    try:

        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
        start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()

        wait = WebDriverWait(driver, 10)
        finish_text_element = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots_lesson_6/dynamic_loading.png")

        actual_text = finish_text_element.text
        assert (
            actual_text == "Hello World!"
        ), f"Ожидался текст 'Hello World!', но был получен '{actual_text}'"

    finally:
        driver.quit()


if __name__ == "__main__":
    test_dynamic_loading()
