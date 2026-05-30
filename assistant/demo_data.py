#Окремий моуль для додавання демо даних, робота з ним описана в README.md section Demo Scenario
import os
import sys
from datetime import datetime, timedelta
# Додати фолдер assistant на пряму щоб використовувати models та storage
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import AddressBook, Record, NotesManager, Note
from storage import save_data, save_notes
def populate_demo_data(book, notes):
    today = datetime.today()
    
    # --- Сценарій 1: Ідеальний контакт (повністю заповнений) ---
    # День народження через 5 днів (потрапить у список birthdays)
    upcoming_bday = (today + timedelta(days=5)).strftime("%d.%m.%Y")
    john = Record("John")
    john.add_phone("1234567890")
    john.add_phone("0987654321")
    john.add_email("john.doe@example.com")
    john.add_address("456 Elm St, San Francisco, CA 94101")
    john.add_birthday(upcoming_bday)
    book.add_record(john)
    
    # --- Сценарій 2: Контакт з мінімальною інформацією ---
    # Тільки ім'я та один телефон.
    jane = Record("Jane")
    jane.add_phone("5551234567")
    book.add_record(jane)
    
    # --- Сценарій 3: Контакт з днем народження, який вже минув ---
    past_bday = (today - timedelta(days=5)).strftime("%d.%m.%Y")
    alice = Record("Alice")
    alice.add_phone("1112223333")
    alice.add_email("alice@wonderland.com")
    alice.add_birthday(past_bday)
    book.add_record(alice)
    
    # --- Сценарій 4: Специфічне форматування адреси та відсутність телефону ---
    bob = Record("Bob")
    bob.add_address("100 Wall St, New York, NY 10005")
    book.add_record(bob)
    
    # --- Сценарій 5: Контакт для видалення ---
    dummy = Record("Dummy")
    dummy.add_phone("9999999999")
    book.add_record(dummy)
    # --- Демо Нотатки ---
    notes.append(Note("Buy groceries for the weekend."))
    notes.append(Note("Project presentation meeting with John scheduled for next Tuesday at 10 AM. Do not forget to prepare slides."))
    notes.append(Note("Urgent: Call Jane regarding the contract!"))
if __name__ == "__main__":
    book = AddressBook()
    notes = NotesManager()
    
    populate_demo_data(book, notes)
    
    save_data(book)
    save_notes(notes)
    print("Demo data successfully generated and saved to addressbook.pkl and notes.pkl.")