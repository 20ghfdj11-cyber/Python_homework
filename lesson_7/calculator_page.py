from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:

    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    RESULT_VALUE = (By.CSS_SELECTOR, ".screen")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 45)

    def open(self):
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        )

    def set_delay(self):
        delay_input = self.wait.until(EC.presence_of_element_located(self.DELAY_INPUT))
        delay_input.clear()
        delay_input.send_keys("45")

    def enter_expression(self):
        buttons = ["7", "+", "8", "="]
        for button in buttons:
            xpath = f"//span[text()='{button}']"
            self.driver.find_element(By.XPATH, xpath).click()

    def get_result(self):
        self.wait.until(EC.text_to_be_present_in_element(self.RESULT_VALUE, "15"))
        result_element = self.driver.find_element(*self.RESULT_VALUE)
        return result_element.text
