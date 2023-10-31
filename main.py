from address_book import AddressBook, Record
from exeptions import ValueNotValid


def has_phone(func):
    def inner(*args, **kwargs):
        try:
            name, phone = args
            result = func(*args, **kwargs)
            return result
        except ValueError:
            return "Not enough values. Expect [name] [phone]"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@has_phone
def add_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    try:
        if record is None:
            record = Record(name)
        
        rez = record.add_phone(phone)
    except Exception as e:
        return e

    if(rez):
        return contacts.add_record(record)
    else:
        return rez
    
   

def delete_contact(args, contacts):
    name, = args
    return contacts.delete(name)

def change_contact(args, contacts):
    try:
        name, phone1, phone2 = args
        record = contacts.find(name)
        _phone1 = record.find_phone(phone1) if record is not None else None
        if _phone1 is not None:
            rez = record.edit_phone(phone1, phone2)
            if rez:
                contacts.add_record(record)
            return rez
        elif record and _phone1 is None:
            return f"Phone {phone1} in \"{name}\" not found"
        else:
            return f"{name} not found"
    except ValueError:
            return "Not enough values. Expect [name] [old_phone] [new_phone]"
    
def show_all(contacts):
    return "".join([f"{contact}\n" for contact in contacts.values()])

def show_phone(args, contacts):
    try:
        name = args[0]
        contact = contacts.find(name)
        return f'"{name}" not found' if contact is None else contact
    except:
        pass

def phone_delete(args, contacts):
    try:
        name, phone = args
        record = contacts.find(name)
        _phone = record.find_phone(phone) if record is not None else None
        if _phone is not None:
            rez = record.remove_phone(phone)
            if rez:
                contacts.add_record(record)
                return f"{name} phone {phone} was removed"
        elif record and _phone is None:
            return f"Phone {phone} in \"{name}\" not found"
        else:
            return f"{name} not found"
    except ValueError:
        return "Not enough values. Expect [name] [phone]"


def set_email(args, contacts): 
    try:
        name, email = args
        record = contacts.find(name)

        if record is not None:
            rez = record.set_email(email)
            if rez:
                contacts.add_record(record)
            return rez
        return f'"{name}" not found'
    except ValueNotValid as e:
        return e 
    except ValueError as e:
        return "Not enough values. Expect [name] [email]" 


def remove_email(args, contacts):
    try:
        name, = args
        record = contacts.find(name)

        if record is not None:
            rez = record.remove_email()
            if rez:
                contacts.add_record(record)
            return rez
        return f'"{name}" not found'
    except ValueError:
        return "Not enough values. Expect [name]" 
    
def set_address(args, contacts): 
    try:
        name, address = args
        record = contacts.find(name)

        if record is not None:
            rez = record.set_address(address)
            if rez:
                contacts.add_record(record)
            return rez
        return f'"{name}" not found'
    except ValueError:
        return "Not enough values. Expect [name] [address]" 
# remove_address

def add_birthday(args, contacts): 
    try:
        name, birthday = args
        record = contacts.find(name)

        if record is not None:
            rez = record.add_birthday(birthday)
            if rez:
                contacts.add_record(record)
            return rez
        return f'"{name}" not found'
    except ValueError:
        return "Not enough values. Expect [name] [birthday]" 

def show_birthday(args,contacts):
    try:
        name, = args
        record = contacts.find(name)
        if record is not None:
            return record.show_birthday()
        return f'"{name}" not found'
    except ValueError:
        return "Not enough values. Expect [name] [birthday]" 

def birthdays(contacts):
    contacts.get_birthdays_per_week()

def show_help():
    return '''
# hello
# add [name] [phone]
# delete [name]
# change [name] [old_phone] [new_phone]
# phone [name] 
# phone_delete [name] [phone]
# add-birthday [name] [d.m.Y]
# show-birthday [name]
# birthdays 
# all
# exit
'''


def main():
    print("Welcome to the assistant bot!\nPrint 'show_help' for show commands list")
    
    contacts = AddressBook()
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ["exit", "close"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add": #
            print(add_contact(args, contacts))
        elif command == "delete": #
            print(delete_contact(args, contacts))      
        elif command == "change": #
            print(change_contact(args, contacts))
        elif command == "phone": #
            print(show_phone(args, contacts))
        elif command == "phone_delete": #
            print(phone_delete(args, contacts))
        elif command == "add-birthday": #
            print(add_birthday(args, contacts))       
        elif command == "show-birthday": #
            print(show_birthday(args,contacts))
        elif command == "birthdays":
            birthdays(contacts)
        elif command == "all":
            print(show_all(contacts))
        elif command == "set-email": 
            print(set_email(args,contacts))
        elif command == "remove-email": 
            print(remove_email(args,contacts))
        elif command == "set-address": 
            print(set_address(args,contacts))
        elif command == "remove-address": 
            # print(remove_address(args,contacts))
            pass
        elif command == "show_help":
            print(show_help())
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
