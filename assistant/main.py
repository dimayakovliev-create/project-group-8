from command_parser import parse_input
from handlers import (
    add_contact, change_contact, show_phone, show_all,
    add_birthday, show_birthday, birthdays, delete_contact,
    search_contacts, add_email, add_address,
    add_note, change_note, delete_note, search_notes, show_all_notes, show_help
)
from models import AddressBook, NotesManager
from storage import save_data, load_data, save_notes, load_notes
import colorama
from colorama import Fore
from prompt_toolkit import prompt, HTML
from prompt_toolkit.completion import NestedCompleter

def main():
    colorama.init(autoreset=True)
    # Завантажуємо адресну книгу та нотатки перед початком
    book = load_data()
    notes = load_notes()
    print(Fore.CYAN + "Welcome to the assistant bot!")
    
    while True:
        # Створюємо словник для підказок, де ключі — це імена існуючих контактів.
        # Значення None вказує на те, що після імені автозавершення не потрібне.
        contacts_dict = {name: None for name in book.data.keys()}

        # Створюємо словник для NestedCompleter, який містить усі можливі команди.
        # Команди, які працюють з конкретними контактами, отримують contacts_dict для підказок.
        completer_dictionary = {
            "add": contacts_dict,
            "change": contacts_dict,
            "phone": contacts_dict,
            "add-email": contacts_dict,
            "add-address": contacts_dict,
            "add-birthday": contacts_dict,
            "show-birthday": contacts_dict,
            "delete": contacts_dict,
            "search": None,
            "all": None,
            "birthdays": None,
            "add-note": None,
            "change-note": None,
            "delete-note": None,
            "search-note": None,
            "notes": None,
            "hello": None,
            "exit": None,
            "close": None,
            "help": None
        }
        # Ініціалізуємо об'єкт автозавершення
        command_completer = NestedCompleter.from_nested_dict(completer_dictionary)
        
        try:
            # Використовуємо prompt() замість звичайного input() для підтримки автозавершення клавішею Tab
            user_input = prompt(HTML("<ansiyellow>Enter a command: </ansiyellow>"), completer=command_completer).strip()
        except (KeyboardInterrupt, EOFError):
            # Захист від Ctrl+C або Ctrl+D — гарантує, що дані збережуться при примусовому закритті програми
            save_data(book)
            save_notes(notes)
            print(Fore.CYAN + "\nGood bye!")
            break

        # Захист від порожнього вводу (наприклад, якщо користувач просто натиснув Enter)
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
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "search":
            print(search_contacts(args, book))
        elif command == "add-note":
            print(add_note(args, notes))
        elif command == "change-note":
            print(change_note(args, notes))
        elif command == "delete-note":
            print(delete_note(args, notes))
        elif command == "search-note":
            print(search_notes(args, notes))
        elif command == "notes":
            print(show_all_notes(notes))
        elif command == "help":
            print(show_help())
        else:
            print(Fore.RED + "Invalid command.")

if __name__ == "__main__":
    main()