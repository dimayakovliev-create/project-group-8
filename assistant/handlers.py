from models import AddressBook, Record

#Декоратор який перехоплює вийнятки та повертає відповідні повідомлення
def error_handler(func):
    def errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) and "unpack" not in str(e):
                return str(e)
            return "Error: Please provide name and phone number."
        except IndexError:
            return "Error: Please provide a name."
        except KeyError:
            return "Error: Contact not found."
        
    return errors

#Додає новий контакт до адресної книги.
@error_handler
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError
    
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)

    return message

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

    return "Contact updated."

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
        return "No phones found."
    
    return "; ".join(p.value for p in record.phones)

#Повертає рядок з усіма збереженими контактами.
@error_handler
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    
    return "\n".join(str(record) for record in book.data.values())

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

    return "Birthday added."

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
        return "No birthday found."
    
    return record.birthday.value.strftime('%d.%m.%Y')

# Показує дні народження на наступному тижні
@error_handler
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."
    
    result = []

    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")

    return "\n".join(result)

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

    return "Contact deleted."