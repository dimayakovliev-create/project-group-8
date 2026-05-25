from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту.
class Name(Field):
    pass

# Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

# Клас для зберігання дати народження.
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Клас для зберігання інформації про контакт, включно з іменем та списком телефонів. 
# Містить методі маніпуляцій з записами, в класі задане поле name та атрибут phones
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    # Метод який дозволяє додавати номер. phone_number передається як аргумент методу а
    # не доданий як поле класу щоб зберігати килька номерів в phones а не тільки один при ініціалізації обʼєкту Record
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    # Видаляємо номер телефону якщо він співпажає з існуючим в списку phones, якщо після проходження по всім елементам 
    # списку співпадінь не знайдено то кидаємо ексепшн
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
            
        raise ValueError(f"Phone {phone_number} not found.")

    # Оновлюємо номер телефону знаходячи його індекс по списку номерів для того щоб замінити по індексу а не по номеру.
    # Це дозволяє не змінювати порядок номерів на відміну від phones.append який би додав оновлений номер в кінець списку
    # після видалення
    def edit_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
            
        raise ValueError(f"Phone {old_phone} not found.")

    # Повертаємо номер телефону якщо він є в списку
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
            
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # HW07 Додаємо метод який для контактів адресної книги повертає список користувачів, 
    # яких потрібно привітати по днях на наступному тижні.
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday_date = record.birthday.value.date()

            try:
                birthday_this_year = bday_date.replace(year=today.year)
            except ValueError:
                # Handle Feb 29 on non-leap years
                birthday_this_year = bday_date.replace(year=today.year, day=28)

            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                except ValueError:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1, day=28)

            days_until = (birthday_this_year - today).days

            if 0 <= days_until <= 7:
                weekday = birthday_this_year.weekday()
                if weekday == 5:
                    congratulation_date = birthday_this_year + timedelta(days=2)
                elif weekday == 6:
                    congratulation_date = birthday_this_year + timedelta(days=1)
                else:
                    congratulation_date = birthday_this_year

                upcoming.append({"name": record.name.value, "congratulation_date": congratulation_date.strftime("%d.%m.%Y")})

        return upcoming

#Приклад
if __name__ == "__main__":
    # Додамо запис з днем народження, який настане через 2 дні
    upcoming_date = (datetime.today().date() + timedelta(days=2)).strftime("%d.%m.%Y")

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    # Зміги з HW07
    # Перевірка додавання дня народження (add-birthday)
    john_record.add_birthday("25.05.1990")

    # Створення запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    # Створення запису для Alice
    alice_record = Record("Alice")
    alice_record.add_phone("1231231234")
    alice_record.add_birthday(upcoming_date)
        
    # Додавання створених записів до адресної книги
    book.add_record(john_record)
    book.add_record(jane_record)
    book.add_record(alice_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Перевірка показу дня народження (show-birthday)
    if john.birthday:
        print(f"John's birthday: {john.birthday.value.strftime('%d.%m.%Y')}")

    # Перевірка списку найближчих днів народження (birthdays)
    print("Upcoming birthdays:", book.get_upcoming_birthdays())
