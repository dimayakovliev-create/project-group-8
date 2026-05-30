from models import AddressBook, Record, Note, NotesManager
from tabulate import tabulate
from colorama import Fore

#Декоратор який перехоплює вийнятки та повертає відповідні повідомлення
def error_handler(func):
    def errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) and "unpack" not in str(e):
                return Fore.RED + str(e)
            return Fore.RED + "Error: Please provide name and phone number."
        except IndexError:
            return Fore.RED + "Error: Please provide a name."
        except KeyError:
            return Fore.RED + "Error: Contact not found."
        
    return errors

#Додає новий контакт до адресної книги.
@error_handler
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError
    
    name, phone, *_ = args
    record = book.find(name)
    is_new = False

    if record is None:
        record = Record(name)
        is_new = True

    if phone:
        # Спробуємо додати телефон. Якщо буде помилка валідації, вона перерве виконання
        # і запис не буде додано до книги.
        record.add_phone(phone)

    if is_new:
        book.add_record(record)
        return Fore.GREEN + "Contact added."
    else:
        return Fore.GREEN + "Contact updated."

#Змінює номер існуючого контакту.
@error_handler
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Error: Please provide name, old phone and new phone.")
    
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError
    
    record.edit_phone(old_phone, new_phone)

    return Fore.GREEN + "Contact updated."

#Повертає номер телефону за ім'ям.
@error_handler
def show_phone(args, book: AddressBook):
    if not args:
        raise IndexError
    
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError
    
    if not record.phones:
        return Fore.YELLOW + "No phones found."
    
    return "; ".join(p.value for p in record.phones)

#Повертає рядок з усіма збереженими контактами.
@error_handler
def show_all(book: AddressBook):
    if not book.data:
        return Fore.YELLOW + "No contacts found."
    
    table = []
    for record in book.data.values():
        phones = "; ".join(p.value for p in record.phones)
        birthday = getattr(record, 'birthday', None)
        birthday_str = birthday.value.strftime('%d.%m.%Y') if birthday else ""
        email = getattr(record, 'email', None)
        email_str = email.value if email else ""
        address = getattr(record, 'address', None)
        address_str = address.value if address else ""
        table.append([record.name.value, phones, birthday_str, email_str, address_str])
        
    return tabulate(table, headers=["Name", "Phones", "Birthday", "Email", "Address"], tablefmt="grid")

# Додає електронну пошту до контакту
@error_handler
def add_email(args, book: AddressBook):
    if len(args) < 2:
        return Fore.RED + "Error: Please provide name and email."
    
    name, email_str, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError
    
    record.add_email(email_str)

    return Fore.GREEN + "Email added."

# Додає адресу до контакту
@error_handler
def add_address(args, book: AddressBook):
    if len(args) < 2:
        return Fore.RED + "Error: Please provide name and address."
    
    name = args[0]
    address_str = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        raise KeyError
    
    record.add_address(address_str)

    return Fore.GREEN + "Address added."

#Зміни HW07
# Додає дату народження до контакту
@error_handler
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Error: Please provide name and birthday.")
    
    name, birthday_str, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError
    
    record.add_birthday(birthday_str)

    return Fore.GREEN + "Birthday added."

# Показує дату народження контакту
@error_handler
def show_birthday(args, book: AddressBook):
    if not args:
        raise IndexError
    
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError
    if record.birthday is None:
        return Fore.YELLOW + "No birthday found."
    
    return record.birthday.value.strftime('%d.%m.%Y')

# Показує дні народження на наступному тижні
@error_handler
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return Fore.YELLOW + "No upcoming birthdays."
    
    table = []
    for item in upcoming:
        table.append([item['name'], item['congratulation_date']])

    return tabulate(table, headers=["Name", "Congratulation Date"], tablefmt="grid")

# Видаляє контакти
@error_handler
def delete_contact(args, book: AddressBook):
    if not args:
        raise IndexError
    
    name = args[0]
    
    # Перевіряємо чи існує такий контакт перед видаленням
    if book.find(name) is None:
        raise KeyError
        
    book.delete(name)

    return Fore.GREEN + "Contact deleted."

# Шукає контакти за частковим збігом імені або номера телефону
@error_handler
def search_contacts(args, book: AddressBook):
    if not args:
        raise ValueError("Error: Please provide a search query.")
    
    query = " ".join(args)
    results = book.search(query)
    
    if not results:
        return Fore.YELLOW + "No contacts found matching your query."
    
    table = []
    for record in results:
        phones = "; ".join(p.value for p in record.phones)
        birthday = getattr(record, 'birthday', None)
        birthday_str = birthday.value.strftime('%d.%m.%Y') if birthday else ""
        email = getattr(record, 'email', None)
        email_str = email.value if email else ""
        address = getattr(record, 'address', None)
        address_str = address.value if address else ""
        table.append([record.name.value, phones, birthday_str, email_str, address_str])
        
    return tabulate(table, headers=["Name", "Phones", "Birthday", "Email", "Address"], tablefmt="grid")

# === ОБРОБНИКИ ДЛЯ НОТАТОК ===

def note_error_handler(func):
    def errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return Fore.RED + "Error: Invalid note number."
        except IndexError:
            return Fore.RED + "Error: Note not found (invalid index)."
    return errors

@note_error_handler
def add_note(args, notes: NotesManager):
    if not args:
        return Fore.RED + "Error: Please provide note text."
    text = " ".join(args)
    note = Note(text)
    notes.append(note)
    return Fore.GREEN + "Note added."

@note_error_handler
def change_note(args, notes: NotesManager):
    if len(args) < 2:
        return Fore.RED + "Error: Please provide note number and new text."
    index = int(args[0]) - 1
    if index < 0 or index >= len(notes):
        raise IndexError
    new_text = " ".join(args[1:])
    notes[index] = Note(new_text)
    return Fore.GREEN + "Note updated."

@note_error_handler
def delete_note(args, notes: NotesManager):
    if not args:
        return Fore.RED + "Error: Please provide a note number."
    index = int(args[0]) - 1
    if index < 0 or index >= len(notes):
        raise IndexError
    notes.pop(index)
    return Fore.GREEN + "Note deleted."

@note_error_handler
def search_notes(args, notes: NotesManager):
    if not args:
        return Fore.RED + "Error: Please provide a search query."
    query = " ".join(args)
    results = notes.search(query)
    if not results:
        return Fore.YELLOW + "No notes found matching your query."
    
    table = []
    for i, note in results:
        table.append([i + 1, note.value])
        
    return tabulate(table, headers=["ID", "Note Text"], tablefmt="grid")

@note_error_handler
def show_all_notes(notes: NotesManager):
    if not notes.data:
        return Fore.YELLOW + "No notes found."
    
    table = []
    for i, note in enumerate(notes.data):
        table.append([i + 1, note.value])
        
    return tabulate(table, headers=["ID", "Note Text"], tablefmt="grid")