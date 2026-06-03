from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 14", "+79190000001"),
    Smartphone("Samsung", "Galaxy S21", "+79190000002"),
    Smartphone("Xiaomi", "Redmi Note 11", "+79190000003"),
    Smartphone("Google", "Pixel 6", "+79190000004"),
    Smartphone("Nokia", "3310", "+79190000005")
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.number}")