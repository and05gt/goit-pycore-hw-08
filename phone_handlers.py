from address_book import AddressBook, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."

    return inner

def parse_input(user_input: str) -> str:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook) -> str:
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Usage: add [name] [phone]")
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

@input_error
def change_contact(args: list, book: AddressBook) -> str:
    if len(args) != 3:
        raise ValueError("Invalid number of arguments. Usage: change [name] [old_phone] [new_phone]")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError()

@input_error
def show_phone(args: list, book: AddressBook) -> str:
    if len(args) != 1:
        raise ValueError("Invalid number of arguments. Usage: phone [name]")
    name = args[0]
    record = book.find(name)
    if record:
        return record.phones[0].value
    else:
        raise KeyError()

@input_error
def show_all(_, book: AddressBook) -> str:
    if book:
        return "\n".join(f"{name}: {record.phones[0].value}" for name, record in book.items())
    else:
        return "No contacts found."
    
@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Usage: add-birthday [name] [birthday]")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError()
    
@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    if len(args) != 1:
        raise ValueError("Invalid number of arguments. Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday is None:
            return "Birthday not set."
        return record.birthday
    else:
        raise KeyError()
    
@input_error
def birthdays(_args: list, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return upcoming_birthdays
    else:
        return "No upcoming birthdays."