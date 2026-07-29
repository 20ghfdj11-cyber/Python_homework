from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from typing import Final


class MainShopPage:
    """Класс Page Object для главной страницы магазина SauceDemo."""

    LOGIN_INPUT: Final = (By.CSS_SELECTOR, "#user-name")
    PASSWORD_INPUT: Final = (By.CSS_SELECTOR, "#password")
    LOGIN_BUTTON: Final = (By.CSS_SELECTOR, "#login-button")
    ADD_BACKPACK_BUTTON: Final = (By.NAME, "add-to-cart-sauce-labs-backpack")
    ADD_BOLT_T_SHIRT_BUTTON: Final = (
        By.NAME,
        "add-to-cart-sauce-labs-bolt-t-shirt",
    )
    ADD_ONESIE_BUTTON: Final = (By.NAME, "add-to-cart-sauce-labs-onesie")

    def __init__(self, driver, url: str):
        """
        Инициализирует страницу, сохраняет драйвер и открывает указанный URL.

        Args:
            driver: экземпляр WebDriver.
            url: адрес страницы для открытия при создании объекта.
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.url)

    @allure.step("Открытие страницы оформления заказа")
    def open(self) -> None:
        """
        Переходит на страницу оформления заказа (checkout-step-one).
        Используется вместо стандартного открытия главной страницы.
        """
        self.driver.get("https://www.saucedemo.com/checkout-step-one.html")

    @allure.step("Авторизация пользователя")
    def authorization(self) -> None:
        """
        Выполняет ввод учетных данных standard_user / secret_sauce
        и нажимает кнопку входа.
        """
        login_input = self.wait.until(EC.presence_of_element_located(self.LOGIN_INPUT))
        login_input.send_keys("standard_user")

        password_input = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        password_input.send_keys("secret_sauce")

        login_button = self.wait.until(
            EC.presence_of_element_located(self.LOGIN_BUTTON)
        )
        login_button.click()

    @allure.step("Добавление товаров в корзину")
    def get_add_product(self) -> None:
        """
        Последовательно добавляет три определенных товара в корзину.
        """
        self.wait.until(
            EC.presence_of_element_located(self.ADD_BACKPACK_BUTTON)
        ).click()
        self.wait.until(
            EC.presence_of_element_located(self.ADD_BOLT_T_SHIRT_BUTTON)
        ).click()
        self.wait.until(EC.presence_of_element_located(self.ADD_ONESIE_BUTTON)).click()


class CartPage:
    """Класс Page Object для страницы корзины и оформления заказа."""

    SHOPPING_CART_BUTTON: Final = (By.ID, "shopping_cart_container")
    CHECKOUT_BUTTON: Final = (By.ID, "checkout")
    FIRST_NAME_INPUT: Final = (By.CSS_SELECTOR, "#first-name")
    LAST_NAME_INPUT: Final = (By.CSS_SELECTOR, "#last-name")
    POSTAL_CODE_INPUT: Final = (By.CSS_SELECTOR, "#postal-code")
    CONTINUE_BUTTON: Final = (By.CSS_SELECTOR, "#continue")
    TOTAL_VALUE: Final = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver, url: str):
        """
        Инициализирует страницу корзины.

        Args:
            driver: экземпляр WebDriver.
            url: прямой URL страницы корзины.
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.url)

    @allure.step("Открытие модального окна корзины")
    def get_shopping_card(self) -> None:
        """
        Нажимает на иконку корзины для отображения списка товаров.
        """
        self.wait.until(
            EC.presence_of_element_located(self.SHOPPING_CART_BUTTON)
        ).click()

    @allure.step("Переход к оформлению заказа (Checkout)")
    def get_checkout(self) -> None:
        """
        Нажимает кнопку Checkout для перехода к заполнению данных.
        """
        self.wait.until(EC.presence_of_element_located(self.CHECKOUT_BUTTON)).click()

    @allure.step("Заполнение формы доставки")
    def get_form(self) -> None:
        """
        Заполняет форму контактными данными: имя, фамилия, почтовый индекс.
        """
        first_name_input = self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME_INPUT)
        )
        first_name_input.send_keys("Kirill")  # Исправлено fist -> first

        last_name_input = self.wait.until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        )
        last_name_input.send_keys("Stanin")

        postal_code_input = self.wait.until(
            EC.presence_of_element_located(self.POSTAL_CODE_INPUT)
        )
        postal_code_input.send_keys("456537")

    @allure.step("Переход к обзору заказа (Continue)")
    def get_continue(self) -> None:
        """
        Нажимает кнопку Continue для перехода к финальному обзору.
        """
        self.wait.until(EC.presence_of_element_located(self.CONTINUE_BUTTON)).click()

    @allure.step("Ожидание появления итоговой суммы")
    def get_total(self) -> None:
        """
        Ожидает, пока элемент с итоговой суммой появится на странице.
        """
        self.wait.until(EC.presence_of_element_located(self.TOTAL_VALUE))

    @allure.step("Получение текста итоговой суммы")
    def get_result(self) -> str:
        """
        Ожидает конкретный текст суммы и возвращает его полное содержимое.

        Returns:
            str: полный текст элемента с итоговой стоимостью (например, 'Total: $58.29').
        """
        self.wait.until(
            EC.text_to_be_present_in_element(self.TOTAL_VALUE, "Total: $58.29")
        )
        result_element = self.driver.find_element(*self.TOTAL_VALUE)
        return result_element.text
