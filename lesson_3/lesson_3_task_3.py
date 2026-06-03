from address import Address
from mailing import Mailing

to_addr = Address("105000", "Казань", "Проспект Ямашева", "12", "34")
from_addr = Address("101000", "Пермь", "Тверская улица", "7", "21")

mail = Mailing(
    to_address=to_addr,
    from_address=from_addr,
    cost=250.75,
    track="AB123456789RU"
)

print(f"Отправление {mail.track} из {mail.from_address.index}, {mail.from_address.city}, "
      f"{mail.from_address.street}, {mail.from_address.house} - {mail.from_address.apartment} "
      f"в {mail.to_address.index}, {mail.to_address.city}, "
      f"{mail.to_address.street}, {mail.to_address.house} - {mail.to_address.apartment}. "
      f"Стоимость {mail.cost} рублей.")