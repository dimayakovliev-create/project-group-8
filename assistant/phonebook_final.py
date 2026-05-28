from collections import UserDict
from datetime import datetime, timedelta
import re


# HW07! Доданий декоратор для обробки помилок введення користувача:
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please provide all required arguments."
    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Ствоорення класу Name, який є обов'язковим полем для контакту (не може бути порожнім) та успадковує Field
class Name(Field):
    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())

# HW07! Створення класу Birthday, який успадковує Field та має валідацію для дати народження (наприклад, формат DD.MM.YYYY)
class Birthday(Field):
    def __init__(self, value):
        try:
            self.birthday = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(self.birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
   

# Створення класу Phone, який успадковує Field та має валідацію для телефонного номера (наприклад, 10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

# Необов'язкове поле Email з валідацією формату електронної пошти
class Email(Field):
    def __init__(self, value):
        # Прроста валідація формату email за допомогою регулярного виразу
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

# Клас Record для зберігання інформації про контакт, який містить ім'я, список телефонів та список email
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []  # Список для зберігання email адрес, оскільки контакт може мати кілька email
        self.birthday = None  # HW07! Поле для зберігання дати народження
    
    # керування телефонів (додавання, видалення, редагування)
    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return True
        return False

    def edit_phone(self, old_phone_number, new_phone_number):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_number:
                self.phones[i] = Phone(new_phone_number)
                return True
        return False
        
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    # керування Email (додавання, видалення, редагування)
    def add_email(self, email_address):
        email = Email(email_address)
        self.emails.append(email)

    def remove_email(self, email_address):
        for email in self.emails:
            if email.value == email_address:
                self.emails.remove(email)
                return True
        return False
    
    def edit_email(self, old_email, new_email):
        for i, email in enumerate(self.emails):
            if email.value == old_email:
                self.emails[i] = Email(new_email)
                return True
        raise ValueError(f"Email {old_email} not found.")

    # HW07! Додавання методу для встановлення дати народження
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    # HW07! Додавання методу для пошуку дати народження
    def show_birthday(self):
        return self.birthday
    
    # HW07! Додавання методу для редагування дати народження
    def edit_birthday(self, new_birthday_str):
        self.birthday = Birthday(new_birthday_str)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones) if self.phones else "None"
        emails_str = '; '.join(e.value for e in self.emails) if self.emails else "None"
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "None" # HW07! Форматування дати народження для виводу
        return f"Contact name: {self.name.value}, Phones: {phones_str}, Emails: {emails_str}, Birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    # Універсальний пошук по імені, телефону та email
    def search(self, query):
        query = query.lower()
        results = []
        
        for record in self.data.values():
            # Перевіряємо ім'я на відповідність запиту (ігноруємо регістр)
            if query in record.name.value.lower():
                results.append(record)
                continue
            
            # Перевіряємо телефони  на відповідність запиту (ігноруємо регістр) та підтримуємо частковий пошук
            phone_match = any(query in phone.value for phone in record.phones)
            if phone_match:
                results.append(record)
                continue
                
            # Перевіряємо email на відповідність запиту (ігноруємо регістр) та підтримуємо частковий пошук
            email_match = any(query in email.value.lower() for email in record.emails)
            if email_match:
                results.append(record)
                continue
                
        return results

    # HW07! Додавання методу для отримання списку контактів, у яких день народження припадає на найближчі 7 днів:
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        
        for record in self.data.values():
            if not record.birthday:
                continue
                
            birthday_this_year = record.birthday.value.date()
            birthday_this_year = birthday_this_year.replace(year=today.year)
            
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
            days_until = (birthday_this_year - today).days
            
            if 0 <= days_until <= 7:
                weekday_this_year = birthday_this_year.weekday()
                congrat_date = birthday_this_year
                
                if weekday_this_year == 5:
                    congrat_date = birthday_this_year + timedelta(days=2)
                elif weekday_this_year == 6:
                    congrat_date = birthday_this_year + timedelta(days=1)
                
                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congrat_date.strftime("%d.%m.%Y")
                })
                
        return upcoming


# HW07! Додані функції-обробники команд користувача:
def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added successfully."
    else:
        message = "Contact updated."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated successfully."


@input_error
def show_phone(args, book):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}'s phones: {', '.join(p.value for p in record.phones)}"


def show_all(book):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise IndexError
    name, birthday_str = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError
    record.set_birthday(birthday_str)
    return f"Birthday for {name} added successfully."


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.birthday:
        return f"No birthday set for {name}."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
    
    result = ["Upcoming birthdays:"]
    for item in upcoming:
        result.append(f"{item['name']}: congratulation date {item['congratulation_date']}")
    return "\n".join(result)


# HW07! Головна функція для запуску бота та обробки команд користувача:
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue
            
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(*args, book))
        elif command == "change":
            print(change_contact(*args, book))
        elif command == "phone":
            print(show_phone(*args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(*args, book))
        elif command == "show-birthday":
            print(show_birthday(*args, book))
        elif command == "birthdays":
            print(birthdays(*args, book))
        else:
            print("Invalid command. Enter the argument for the command: add, change, phone, all, add-birthday, show-birthday, birthdays, exit, close, hello")

if __name__ == "__main__":
    main()
