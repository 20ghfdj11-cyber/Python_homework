import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def test_navigation():
    driver = webdriver.Chrome()
    try:
        driver.get("https://httpbin.org/")
        time.sleep(3)

        try:
            link = driver.find_element(By.LINK_TEXT, "HTML form")
            link.click()
            time.sleep(3)
            if "/forms/post" not in driver.current_url:
                raise ValueError("Не та страница.")
        except (NoSuchElementException, ValueError) as e:
            print(f"Ошибка при навигации: {e}")
        finally:
            driver.back()
            time.sleep(3)
    finally:
        driver.quit()


if __name__ == "__main__":
    test_navigation()
