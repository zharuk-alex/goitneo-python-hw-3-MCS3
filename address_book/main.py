from collections import UserDict
import os
import pickle
import datetime
from birthdays import get_birthdays_per_week
import json


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    phone_len = 10

    def __init__(self, phone):
        validated = self.validate(phone)
        super().__init__(validated)

    def validate(self, phone):
        if len(phone) == Phone.phone_len and phone.isdigit():
            return phone
        raise ValueError(f"The correct phone number must contain {Phone.phone_len} numbers")


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
        self.birthday = None

    def add_phone(self, phone):
        try:
            _phone = Phone(phone)
            self.phones.append(_phone)
            return "Phone added successfully"
        except Exception as e:
            raise e
    
    def remove_phone(self, phone):
        for _phone in self.phones:
            if _phone.value == phone:
                return self.phones.remove(_phone)
        return "Phone not found"

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"



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

