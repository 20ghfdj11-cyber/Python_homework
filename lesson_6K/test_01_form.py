import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form():
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

    wait = WebDriverWait(driver, 20)

    firstname_input = wait.until(
        EC.presence_of_element_located((By.NAME, "first-name"))
    )
    firstname_input.send_keys("Иван")

    lastname_input = wait.until(EC.presence_of_element_located((By.NAME, "last-name")))
    lastname_input.send_keys("Петров")

    address_input = wait.until(EC.presence_of_element_located((By.NAME, "address")))
    address_input.send_keys("Ленина, 55-3")

    email_input = wait.until(EC.presence_of_element_located((By.NAME, "e-mail")))
    email_input.send_keys("test@skypro.com")

    city_input = wait.until(EC.presence_of_element_located((By.NAME, "city")))
    city_input.send_keys("Москва")

    country_input = wait.until(EC.presence_of_element_located((By.NAME, "country")))
    country_input.send_keys("Россия")

    phone_input = wait.until(EC.presence_of_element_located((By.NAME, "phone")))
    phone_input.send_keys("+7985899998787")

    job_input = wait.until(EC.presence_of_element_located((By.NAME, "job-position")))
    job_input.send_keys("QA")

    company_input = wait.until(EC.presence_of_element_located((By.NAME, "company")))
    company_input.send_keys("SkyPro")

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], button"))
    )
    submit_button.click()

    zip_code_field = driver.find_element(By.ID, "zip-code")
    color_zip_code = zip_code_field.value_of_css_property("border-color")
    assert color_zip_code == "rgb(245, 194, 199)" in color_zip_code

    fields = [
        "first-name",
        "last-name",
        "address",
        "city",
        "country",
        "e-mail",
        "phone",
        "job-position",
        "company",
    ]

    for field_id in fields:
        field_element = wait.until(EC.visibility_of_element_located((By.ID, field_id)))
        border_color = field_element.value_of_css_property("border-color")
        assert border_color == "rgb(186, 219, 204)", f"Поле {field_id} не зелёное"

    driver.quit()
