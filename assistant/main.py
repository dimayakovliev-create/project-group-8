from command_parser import parse_input
from handlers import (
    add_contact, change_contact, show_phone, show_all,
    add_birthday, show_birthday, birthdays, delete_contact,
    search_contacts, add_email, add_address,
    add_note, change_note, delete_note, search_notes, show_all_notes
)
from models import AddressBook, NotesManager
from storage import save_data, load_data, save_notes, load_notes
import colorama
from colorama import Fore

def main():
    colorama.init(autoreset=True)
    # Завантажуємо адресну книгу та нотатки перед початком
    book = load_data()
    notes = load_notes()
    print(Fore.CYAN + "Welcome to the assistant bot!")
    
    while True:
        user_input = input(Fore.YELLOW + "Enter a command: " + Fore.RESET).strip()
        
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
        else:
            print(Fore.RED + "Invalid command.")

if __name__ == "__main__":
    main()