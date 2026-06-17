from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_form_submission():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.org/forms/post")
    time.sleep(2) 

    name_input = driver.find_element(By.NAME, "custname")
    name_input.send_keys("Мальвина") 

    submit_button = driver.find_element(By.XPATH, "//button[text()='Submit order']")
    submit_button.click()

    time.sleep(3) 

    if driver.current_url != "https://httpbin.org/forms/post":
        print("URL успешно изменился.")
    else:
        print("URL остался тем же.")

    driver.quit()

if __name__ == "__main__":
    test_form_submission()