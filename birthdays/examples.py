from get_birthdays_per_week import get_birthdays_per_week
from utils.fetch_data import fakerList, dbList

users_list = dbList() # read .json 
print('\n',("* "*5),"dbList",(" *"*5))
print(("* "*5),"forward 7 days",(" *"*5))
get_birthdays_per_week(users_list) #solution 1: from today 7 days 
print(("* "*5),"next week",(" *"*5))
get_birthdays_per_week(users_list, nextweek=True) #solution 2: next week Mon-Fri & current weekends

users_list = fakerList(50) # Faker
print('\n',("* "*5),"fakerList",(" *"*5))
print(("* "*5),"forward 7 days",(" *"*5))
get_birthdays_per_week(users_list)
print(("* "*5),"next week",(" *"*5))
get_birthdays_per_week(users_list, nextweek=True)
