from selenium import webdriver
from selenium.webdriver.common.by import By

def test_multiple_elements():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.org/links/10")

    links = driver.find_elements(By.TAG_NAME, "a")
    
    print(f"Найдено ссылок: {len(links)}")
    assert len(links) == 9, "Количество ссылок не равно 9"

    all_visible = True
    for link in links:
        if not link.is_displayed():
            all_visible = False
            break
    print(f"Все ссылки отображаются: {all_visible}")
    assert all_visible, "Не все ссылки отображаются"

    first_link_text = links[0].text
    print(f"Текст первой ссылки: {first_link_text}")
    assert "1" in first_link_text, "Текст первой ссылки не содержит '1'"

    driver.quit()

if __name__ == "__main__":
    test_multiple_elements()