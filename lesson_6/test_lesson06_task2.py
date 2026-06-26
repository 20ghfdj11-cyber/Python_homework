from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def set_cookies_for_user(driver, cookies):
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)


def wait_for_page_load(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


def test_session_storage_auth():
    driver = webdriver.Chrome()

    try:
        driver.get("https://gitflic.ru/")

        wait = WebDriverWait(driver, 10)
        wait_for_page_load(driver)

        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
        except TimeoutException:
            pass

        cookies_user1 = [
            {
                "name": "SESSION",
                "value": "N2Y1YmUzNTktMDIyNi00NjU0LWJkZWYtMTA2NWFhYmU4NDcz",
                "domain": "gitflic.ru",
            }
        ]
        set_cookies_for_user(driver, cookies_user1)

        driver.refresh()
        wait_for_page_load(driver)

        user1_username = "malvina_sky_pro_1"
        driver.get(f"https://gitflic.ru/user/{user1_username}")
        wait_for_page_load(driver)

        try:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile-header"))
            )
        except TimeoutException:
            pass

        url_user1 = driver.current_url

        driver.delete_all_cookies()
        driver.refresh()
        wait_for_page_load(driver)

        cookies_user2 = [
            {
                "name": "SESSION",
                "value": "Y2E1ZmFjNTAtMDYwYy00MzA4LWE0NDktYmM5NzI5MDZlMGE5",
                "domain": "gitflic.ru",
            }
        ]
        set_cookies_for_user(driver, cookies_user2)

        driver.refresh()
        wait_for_page_load(driver)

        user2_username = "malvina_sky_pro_2"
        driver.get(f"https://gitflic.ru/user/{user2_username}")
        wait_for_page_load(driver)

        try:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile-header"))
            )
        except TimeoutException:
            pass

        url_user2 = driver.current_url

        assert (
            url_user1 != url_user2
        ), "URLs для пользователей совпадают, тест провален!"
        print("Тест успешно выполнен! URL для каждого пользователя отличается.")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_session_storage_auth()
