from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_navigation():
    driver = webdriver.Chrome()
    try:
       
        driver.get("https://httpbin.org/")

        link = driver.find_element(By.LINK_TEXT, "HTML Form")
        link.click()

        assert "/forms/post" in driver.current_url, \
            f"Expected '/forms/post' in URL, but got {driver.current_url}"

        driver.back()

        assert driver.current_url == "https://httpbin.org/", \
            f"Expected URL 'https://httpbin.org/', but got {driver.current_url}"

    finally:
        driver.quit()