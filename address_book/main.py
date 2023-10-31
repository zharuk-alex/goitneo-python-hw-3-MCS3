from collections import UserDict
import os
import pickle
import datetime
import re

from birthdays import get_birthdays_per_week
from exeptions import ValueNotValid


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    value_len = 10

    def __init__(self, value):
        validated = self.validate(value)
        super().__init__(validated)

    def validate(self, value):
        if len(value) == Phone.value_len and value.isdigit():
            return value
        # raise ValueError(f"The correct phone number must contain {Phone.value_len} numbers")
        raise ValueNotValid(f"The correct phone number must contain {Phone.value_len} numbers")
    

class Email(Field):
    def __init__(self, value):
        validated = self.validate(value)
        super().__init__(validated)

    def validate(self, value):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, value):
            return value
        else:
            raise ValueError(f"Invalid email")


class Address(Field):
    value_len = 3
     
    def __init__(self, value):
        validated = self.validate(value)
        super().__init__(validated)

    def validate(self, value):
        if len(value) < Address.value_len:
            return value
        else:
            raise ValueError(f"Address cannot be less than {Address.value_len} characters ")

class Birthday(Field):
    
    def __init__(self, birthday):
        validated = self.validate(birthday)
        super().__init__(validated)
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def validate(self, birthday):
        parsed = datetime.datetime.strptime(birthday, "%d.%m.%Y")
        if parsed:
            return parsed
        raise "This is the incorrect date string format. It should be DD.MM.YYYY"
    
    @property
    def birthday(self):
	    return self.value
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        try:
            _phone = Phone(phone)
            self.phones.append(_phone)
            return "Phone added successfully"
        except Exception as e:
            raise e
    
    def edit_phone(self, phone, new_phone):
        for index, _phone in enumerate(self.phones):
            if _phone.value == phone:
                try:
                    _new_phone = Phone(new_phone)
                    self.phones[index] = _new_phone
                    return "Phone changed successfully"
                except ValueError as e:
                    print(e)
                    raise e
    
    def remove_phone(self, phone):
        for _phone in self.phones:
            if _phone.value == phone:
                return self.phones.remove(_phone)
        return "Phone not found"

    def find_phone(self, phone):
        for _phone in self.phones:
            if _phone.value == phone:
                return _phone
    # 
    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
            return f"{self.name} birthday added"
        except ValueError as e:
            print(e)
            return None
    
    def show_birthday(self):
        return str(self.birthday)
    # 

    def set_email(self, email):
        try:
            self.email = Email(email)
            return "Email setted successfully"
        except Exception as e:
            raise e

    def remove_email(self):
        try:
            if self.email.value is not None:
                self.email = None
                return "Email removed successfully"
        except Exception as e:
            # print(e)
            return f"\"{self.name.value}\" does not have email"

    def set_address(self, value):
        try:
            self.address = Address(value)
            return "Address setted successfully"
        except Exception as e:
            raise e

    def remove_address(self):
        try:
            if self.address.value is not None:
                self.address = None
                return "Address removed successfully"
        except Exception as e:
            print(e)
            return f"\"{self.name.value}\" does not have address"

    def __str__(self):
        rez = "\n"+"*"*10+"\n"
        rez += f"Contact name: {self.name.value}\nphones: {'; '.join(p.value for p in self.phones)}"

        try:
            if(len(self.email.value)):
                rez += f"\nemail: {self.email.value}"
            
            if(len(self.address.value)):
                rez += f"\naddress: {self.address.value}"
        except AttributeError as e:
            # print(e)
            pass
        rez+="\n"+"*"*10
        return rez


class AddressBook(UserDict):
    
    def __init__(self):
        super().__init__()
        path = os.path.realpath(os.path.dirname(__file__))
        self.filename = f'{path}/db.pkl'
        self.read_from_file()
   
           
    def add_record(self, data):
        self.data[data.name] = data
        self.save_to_file()
        return f'"{data.name}" was added'

    def find(self, name):
        for key in self.data.keys():
            if key.value == name:
                return self.data[key]
        return None

    def delete(self, name):
        for _name in self.data:
            if _name.value == name:
                self.data.pop(_name)
                self.save_to_file()
                return f'"{name}" was deleted'
        return None
    
    def birthdays(self):
        return 'Show birthdays per week'
    
    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.data, file)

    def read_from_file(self):
        try:
            with open(self.filename, "rb") as file:
                self.data = pickle.load(file)
        except (EOFError, FileNotFoundError):
            self.data = {}

    def get_birthdays_per_week(self):
        parced_l = list()
       
        for record in self.data.values():
            if(record.__dict__['birthday']):
                parced_l.append({
                    "name": str(record.__dict__['name']),
                    "birthday": record.__dict__['birthday'].birthday
                })
        return get_birthdays_per_week.get_birthdays_per_week(parced_l)

