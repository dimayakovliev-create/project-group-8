from command_parser import parse_input
from handlers import (
    add_contact, change_contact, change_email, show_phone, show_all,
    add_birthday, show_birthday, birthdays, delete_contact,
    search_contacts, add_email, add_address,
    add_note, change_note, delete_note, search_notes, show_all_notes, show_help
)
from models import AddressBook
from storage import delete_data, load_data, save_data, save_notes, load_notes
import colorama
from colorama import Fore
from prompt_toolkit import prompt, HTML
from prompt_toolkit.completion import NestedCompleter
from demo_data import populate_demo_data

def build_completer(book, notes):
# Підказки для телефонів, email, дня народження та нотаток
    phone_hint = {"<phone 10 digits>": None}
    email_hint = {"<email>": None}
    birthday_hint = {"<DD.MM.YYYY>": None}
    note_hint = {"<text>": None}

    contacts_with_existing_phones = {}
    contacts_with_existing_emails = {}

    book_items = book.data.items() if hasattr(book, 'data') else book.items()
    book_keys = book.data.keys() if hasattr(book, 'data') else book.keys()
  
    for name, record in book_items:
        # Підказки для телефонів
        if hasattr(record, 'phones') and record.phones:
            existing_phones = {phone.value: None for phone in record.phones}
            contacts_with_existing_phones[name] = existing_phones
        else:
            contacts_with_existing_phones[name] = phone_hint

        # Підказки для email
        if hasattr(record, 'emails') and record.emails:
            existing_emails = {email.value: None for email in record.emails}
            contacts_with_existing_emails[name] = existing_emails
        else:
            contacts_with_existing_emails[name] = email_hint

    contacts_with_phone = {name: phone_hint for name in book_keys}
    contacts_with_email = {name: email_hint for name in book_keys}
    contacts_with_birthday = {name: birthday_hint for name in book_keys}
    contacts_with_address = {name: None for name in book_keys}
    contacts_no_hints = {name: None for name in book_keys}
    
    note_completer = {}
    if isinstance(notes, list):
        for index, note_text in enumerate(notes):
            note_id = str(index)
            short_text = (note_text[:15] + "...") if len(note_text) > 15 else note_text
            note_completer[f"{note_id} ({short_text})"] = note_hint

    completer_dictionary = {
            "add-contact": contacts_with_phone,
            "change-contact": contacts_with_existing_phones,
            "change-email": contacts_with_existing_emails,
            "show-phone": contacts_with_phone,
            "add-email": contacts_with_email,
            "add-address": contacts_with_address,
            "add-birthday": contacts_with_birthday,
            "show-birthday": contacts_with_birthday,
            "delete": contacts_no_hints,
            "add-note": note_completer,
            "change-note": note_completer,
            "delete-note": note_completer,
            "search-note": note_completer,
            "show-notes": None,
            "delete-addressbook": None,
            "create-demodata": None,
            "search": None,
            "all": None,
            "birthdays": None,
            "hello": None,
            "help": None,
            "exit": None,
            "close": None
    }
    
    return NestedCompleter.from_nested_dict(completer_dictionary)

def main():
    colorama.init(autoreset=True)    # Завантажуємо адресну книгу та нотатки перед початком
    book = load_data()
    notes = load_notes()
    print(Fore.CYAN + "Welcome to the assistant bot!")
    
    need_update_completer = True
    command_completer = None

    while True:
        # Перебудовуємо підказки лише якщо дані змінювалися
        if need_update_completer:
            command_completer = build_completer(book, notes)
            need_update_completer = False

        try:
            user_input = prompt(
                HTML("<ansiyellow>Enter a command: </ansiyellow>"), 
                completer=command_completer
            ).strip()
        except (KeyboardInterrupt, EOFError):
            save_data(book)
            save_notes(notes)
            print(Fore.CYAN + "\nGood bye!")
            break

        if not user_input:
            continue
            
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            # Зберігаємо дані
            save_data(book)
            save_notes(notes)
            print(Fore.CYAN + "Good bye!")
            break
        elif command == "hello":
            print(Fore.CYAN + "How can I help you?")
        elif command == "add-contact":
            print(add_contact(args, book))
            need_update_completer = True
        elif command == "create-demodata":
            populate_demo_data(book, notes)
            save_data(book)
            save_notes(notes)
            print(Fore.GREEN + "Demo data successfully generated and saved.")
        elif command == "change-contact":
            print(change_contact(args, book))
            need_update_completer = True
        elif command == "show-phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "add-email":
            print(add_email(args, book))
            need_update_completer = True
        elif command == "change-email":
            print(change_email(args, book))
            need_update_completer = True
        elif command == "add-address":
            print(add_address(args, book))
            need_update_completer = True
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
            need_update_completer = True
        elif command == "delete-addressbook":
            delete_data()
            book = AddressBook()  # Оновлюємо об'єкт адресної книги після видалення даних
            print(Fore.GREEN + "All contact data has been deleted.")
            need_update_completer = True
        elif command == "search":
            print(search_contacts(args, book))
        elif command == "add-note":
            print(add_note(args, notes))
            need_update_completer = True
        elif command == "change-note":
            print(change_note(args, notes))
            need_update_completer = True
        elif command == "delete-note":
            print(delete_note(args, notes))
            need_update_completer = True
        elif command == "search-note":
            print(search_notes(args, notes))
        elif command == "show-notes":
            print(show_all_notes(notes))
        elif command == "help":
            print(show_help())
        else:
            print(Fore.RED + "Invalid command.")
   
if __name__ == "__main__":
    main()
