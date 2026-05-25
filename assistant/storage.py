# Створено окремий модуль для збереження та завантаження даних
import pickle
from models import AddressBook

# Зберігає дані
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

# Завантажує дані
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Створення нової адресної книги, якщо файл не знайдено