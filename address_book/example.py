from address_book import AddressBook, Record

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")

john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
# john_record.add_phone("33.55555")
# john_record.add_phone("AAAAAAAAAA")

# # Додавання запису John до адресної книги
rez = book.add_record(john_record)
print(type(john_record))
# # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
remove_phone = john.remove_phone("5555555555")

print("before delation")
for name, record in book.data.items():
    print(record)
# # Видалення запису Jane
book.delete("Jane")

print("after delation")
for name, record in book.data.items():
    print(record)

# john.edit_phone("1112223333", "098.7654321")
john.edit_phone("1112223333", "0987654321")
print(john)