import pytest
from string_utils import StringUtils

string_utils = StringUtils()

# Проверка capitalize

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),
    ("hello world", "Hello world"),
    ("python", "Python"),
    ("Тест", "Тест"),
    ("123", "123"),
    ("14 августа 2025", "14 августа 2025"),
])
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected

@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("", ""),
    (" ", " "),
])
def test_capitalize_negative(input_str, expected):
    assert string_utils.capitalize(input_str) == expected

def test_capitalize_with_none():
    with pytest.raises(AttributeError):
        string_utils.capitalize(None)


# Проверка trim

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("   skypro", "skypro"),
    ("  hello", "hello"),
    ("no_spaces", "no_spaces"),
    ("  Тест  ", "Тест  "),
])
def test_trim_positive(input_str, expected):
    assert string_utils.trim(input_str) == expected

@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("", ""),
    (" ", ""),
])
def test_trim_negative(input_str, expected):
    assert string_utils.trim(input_str) == expected

def test_trim_with_none():
    with pytest.raises(AttributeError):
        string_utils.trim(None)


# Проверка contains

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "S", True),
    ("SkyPro", "k", True),
    ("SkyPro", "o", True),
])
def test_contains_positive(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected

@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "z", False),
    ("SkyPro", "U", False),
    ("SkyPro", "x", False),
])
def test_contains_negative(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected


# Проверка delete_symbol

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "k", "SyPro"),
    ("SkyPro", "Pro", "Sky"),
    ("Hello world!", "l", "Heo word!"),
])
def test_delete_symbol_positive(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected

@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "z", "SkyPro"), 
    ("Hello", "x", "Hello"),
    ("Python", "", "Python"),
])
def test_delete_symbol_negative(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected

def contains(self, string: str, symbol: str) -> bool:
    if not isinstance(string, str) or not isinstance(symbol, str):
        raise AttributeError("Both 'string' and 'symbol' must be strings")


def delete_symbol(self, string: str, symbol: str) -> str:
    if not isinstance(string, str) or not isinstance(symbol, str):
        raise AttributeError("Both 'string' and 'symbol' must be strings")