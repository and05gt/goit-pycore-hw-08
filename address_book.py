from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValueError("Name is required")

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Invalid phone number format")
        
class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(self.value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        contact = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            contact += f", birthday: {self.birthday}"

        return contact

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        birthdays_list = []
    
        for name, record in self.data.items():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year).date()
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=birthday_this_year.year + 1)

                difference_date = birthday_this_year.toordinal() - today.toordinal()
                if 0 <= difference_date <= 7:
                    if birthday_this_year.weekday() == 5:
                        birthday_this_year = birthday_this_year.replace(day=birthday_this_year.day + 2)
                    elif birthday_this_year.weekday() == 6:
                        birthday_this_year = birthday_this_year.replace(day=birthday_this_year.day + 1)
                        
                    birthday_this_year = birthday_this_year.strftime("%d.%m.%Y")
                    birthdays_list.append({"name": name, "congratulation_date": birthday_this_year})
        
        return birthdays_list