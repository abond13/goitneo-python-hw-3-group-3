"""
    Домашнє завдання №3
"""
import re
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
#from prompt_toolkit.completion import WordCompleter
#from prompt_toolkit.history import InMemoryHistory
#from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import AddressBook as AB

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name please."
        except KeyError:
            return "No such contact."
        except AB.NameFormatError:
            return "Wrong name format."
        except AB.PhoneFormatError:
            return "Wrong phone format."
        except AB.BirthdayFormatError:
            return "Wrong birthday format."
    return inner

def parse_input(user_input):
    def line_split(line):
        return re.findall(r'[^"\s]\S*|".+?"', line)
    #cmd, *args = user_input.split()
    cmd, *args = line_split(user_input)
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help():
    return "Available commands:\n" + \
           "\tadd [name] [phone]\n" + \
           "\tchange [name] [old_phone] [new_phone]\n" + \
           "\tphone [name]\n" + \
           "\tadd-birthday [name] [birthday]\n" + \
           "\tshow-birthday [name]\n" + \
           "\tbirthdays\n" + \
           "\tall\n" + \
           "\texit"

@input_error
def add_contact(args, book):
    if len(args) == 2:
        name, phone_num = args
        record = book.find(name)
        if not record:
            record = AB.Record(name)
            book.add_record(record)
        record.add_phone(phone_num)
        return "Contact added."
    return "[ERROR] Expected command: add [name] [phone]"

@input_error
def change_contact(args, book):
    if len(args) == 3:
        name, old_phone, new_phone = args
        record = book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return "Contact updated."
        return "[ERROR] No such contact."
    return "[ERROR] Expected command: change [name] [phone]"

@input_error
def phone(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record:
            return record
        return "[ERROR] No such contact."
    return "[ERROR] Expected command: phone [name]"

@input_error
def add_birthday(args, book):
    if len(args) == 2:
        name, birthday = args
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        return "[ERROR] No such contact."
    return "[ERROR] Expected command: add-birthday [name] [birthday]"

@input_error
def show_birthday(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record:
            return record.birthday
        return "[ERROR] No such contact."
    return "[ERROR] Expected command: show-birthday [name]"

@input_error
def birthdays(book):
    book.get_birthdays_per_week()

# completer = WordCompleter(
#     [
#         "close", "exit", "quit", "вийти",
#         "help", "?", "допомога",
#         "add", "додати",
#         "change", "змінити",
#         "phone", "телефон",
#         "add-birthday", "додати–дн",
#         "show-birthday", "показати-дн",
#         "birthdays",
#         "all", "показати-все",
#     ],
#     ignore_case=True,
# )

def main():
    book = AB.AddressBook()
    session = PromptSession()

    print("Welcome to the assistant bot!")
    while True:
        book_completer = book.get_completer()
        completer = NestedCompleter.from_nested_dict(
            {
                "show": {"birthday": book_completer, "all": None},
                "add": None,
                "change": book_completer,
                "phone": book_completer,
                "add-birthday": book_completer,
                "show-birthday": book_completer,
                "birthdays": None,
                "all": None,
                "help" :None, "?": None, "допомога": None,
                "exit": None, "close": None, "quit": None, "вийти": None,
            }
        )
        #user_input = input("Enter a command: ")
        user_input = session.prompt(
            "Enter a command: ", 
            completer=completer,
            complete_while_typing=False,
            # auto_suggest=AutoSuggestFromHistory()
        )
        if user_input:
            command, *args = parse_input(user_input)
        else:
            continue
        if command in ["close", "exit", "quit"]:
            print("Good bye!")
            break
        if command in ["help", "?", "допомога"]:
            print(print_help())
            print(completer)
        elif command in ["add", "додати"]:
            print(add_contact(args, book))
        elif command in ["change", "змінити"]:
            print(change_contact(args, book))
        elif command in ["phone", "телефон"]:
            print(phone(args, book))
        elif command in ["add-birthday", "додати–дн"]:
            print(add_birthday(args, book))
        elif command == ["show-birthday", "показати-дн"]:
            print(show_birthday(args,book))
        elif command == "birthdays":
            birthdays(book)
        elif command in ["all", "показати-все"]:
            print(book)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
