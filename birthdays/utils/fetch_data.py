from datetime import datetime
from faker import Faker
from utils.random_gen import random_date
import json


# data for local test from Faker
def fakerList(n=40):
    fake = Faker()
    users_data = []
    
    for _ in range(n):
        person = {
            'name': fake.name(),
            'birthday': random_date(14, 14)
        }
        users_data.append(person)
    return users_data
#end 


# data for local test from Json
def dbList():
    with open('./db/users.json', 'r') as file:
        users_data = json.load(file)
    
    # Y-m-d str to date instance
    for i in range(len(users_data)):
        users_data[i]['birthday'] = datetime.strptime(users_data[i]['birthday'], '%Y-%m-%d')
    return users_data
#end 