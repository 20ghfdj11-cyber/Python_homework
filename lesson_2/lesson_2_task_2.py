def is_year_leap(year):
    return "True" if year % 4 == 0 else "False"

year = 2024

result = is_year_leap(year)

print(f"год {year}: {result}")