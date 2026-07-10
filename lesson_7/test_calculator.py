import pytest
from selenium import webdriver
from calculator_page import CalculatorPage


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_calculator(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    calc_page = CalculatorPage(driver, url)
    calc_page.open()
    calc_page.set_delay()
    calc_page.enter_expression()
    calc_page.get_result()
    assert calc_page.get_result() == "15"
