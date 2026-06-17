from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_navigation():
    driver = webdriver.Chrome()
    try:
        driver.get("https://httpbin.org/")
        time.sleep(3)

        try:
            link = driver.find_element(By.LINK_TEXT, "HTML form")
            link.click()
            time.sleep(3)
            if "/forms/post" in driver.current_url:
                pass 
            else:
                raise Exception("Страница не та.")
        except:
            pass
        finally:
            driver.back()
            time.sleep(3)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_navigation()