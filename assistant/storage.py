# Створено окремий модуль для збереження та завантаження даних
import pickle
from models import AddressBook, NotesManager

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
    
# Зберігає нотатки
def save_notes(notes, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notes, f)

# Завантажує нотатки
def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NotesManager()  # Створення нового менеджера нотаток, якщо файл не знайдено
