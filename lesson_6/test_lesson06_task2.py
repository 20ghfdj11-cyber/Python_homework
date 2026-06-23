from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def set_cookies_for_user(driver, cookies):

    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)


def main():
    driver = webdriver.Chrome()

    try:

        driver.get("https://gitflic.ru/")
        time.sleep(2)

        cookies_user1 = [
            {
                "name": "SESSION",
                "value": "N2Y1YmUzNTktMDIyNi00NjU0LWJkZWYtMTA2NWFhYmU4NDcz",
                "domain": "gitflic.ru",
            }
        ]
        set_cookies_for_user(driver, cookies_user1)

        driver.refresh()
        time.sleep(2)
        user1_username = "malvina_sky_pro_1"
        driver.get(f"https://gitflic.ru/{user1_username}")
        time.sleep(2)
        url_user1 = driver.current_url

        driver.delete_all_cookies()
        driver.refresh()
        time.sleep(2)

        cookies_user2 = [
            {
                "name": "SESSION",
                "value": "Y2E1ZmFjNTAtMDYwYy00MzA4LWE0NDktYmM5NzI5MDZlMGE5",
                "domain": "gitflic.ru",
            }
        ]
        set_cookies_for_user(driver, cookies_user2)

        driver.refresh()
        time.sleep(2)
        user2_username = "malvina_sky_pro_2"
        driver.get(f"https://gitflic.ru/{user2_username}")
        time.sleep(2)
        url_user2 = driver.current_url

        assert (
            url_user1 != url_user2
        ), "URLs для пользователей совпадают, тест не прошёл!"
        print("Тест успешно выполнен! URL для каждого пользователя отличается.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
