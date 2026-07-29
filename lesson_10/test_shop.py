import pytest
from selenium import webdriver
from shop_page import MainShopPage, CartPage
import allure


@pytest.fixture
def driver():
    """
    Фикстура инициализации драйвера Firefox.
    """
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.title("Проверка полного сценария покупки товаров на SauceDemo")
@allure.description(
    "E2E-тест, проверяющий путь пользователя от главной страницы до "
    "подтверждения итоговой суммы заказа. Тест авторизуется, добавляет три товара "
    "в корзину, переходит к оформлению и проверяет корректность подсчета цены."
)
@allure.feature("Интернет-магазин SauceDemo")
@allure.story("Сценарий оформления заказа тремя товарами")
@allure.severity(allure.severity_level.CRITICAL)
def test_shop(driver):
    """
    Основной тестовый сценарий прохождения цепочки страниц интернет-магазина.

    Args:
        driver: фикстура WebDriver, передаваемая из pytest.
    """
    with allure.step("Инициализация главной страницы магазина"):
        shop_page = MainShopPage(driver, url="https://www.saucedemo.com")

    with allure.step("Открытие целевой страницы"):
        shop_page.open()

    with allure.step("Авторизация пользователя 'standard_user'"):
        shop_page.authorization()

    with allure.step("Добавление трех товаров в корзину"):
        shop_page.get_add_product()

    with allure.step("Переход к странице корзины"):
        shop_page = CartPage(driver, url="https://www.saucedemo.com/cart.html")

    with allure.step("Открытие модального окна корзины"):
        shop_page.get_shopping_card()

    with allure.step("Переход к форме оформления заказа"):
        shop_page.get_checkout()

    with allure.step("Заполнение формы данными покупателя"):
        shop_page.get_form()

    with allure.step("Переход к обзору заказа"):
        shop_page.get_continue()

    with allure.step("Ожидание загрузки итоговой стоимости"):
        shop_page.get_total()

    with allure.step("Получение текста итоговой стоимости"):
        result_text = shop_page.get_result()

    with allure.step(f"Проверка итоговой суммы: ожидание 'Total: $58.29'"):
        assert (
            result_text == "Total: $58.29"
        ), f"Фактическая сумма '{result_text}' не совпадает с ожидаемой"
