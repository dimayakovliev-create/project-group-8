# Створено окремий модуль для збереження та завантаження даних
import os
import pickle
from models import AddressBook, NotesManager

# Завжди отримуємо абсолютний шлях до папки assistant, незалежно від того, звідки запущено скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Зберігає дані
def save_data(book, filename="addressbook.pkl"):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "wb") as f:
        pickle.dump(book, f)

# Завантажує дані
def load_data(filename="addressbook.pkl"):
    filepath = os.path.join(BASE_DIR, filename)
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Створення нової адресної книги, якщо файл не знайдено
    
# Зберігає нотатки
def save_notes(notes, filename="notes.pkl"):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "wb") as f:
        pickle.dump(notes, f)

# Завантажує нотатки
def load_notes(filename="notes.pkl"):
    filepath = os.path.join(BASE_DIR, filename)
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NotesManager()  # Створення нового менеджера нотаток, якщо файл не знайдено
