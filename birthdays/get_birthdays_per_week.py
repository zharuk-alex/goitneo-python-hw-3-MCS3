from datetime import datetime, timedelta
from collections import defaultdict 


def get_birthdays_per_week(
        users:list, 
        # False - calc for 7 days / True - calc current weekend and next week Mon-Fri
        nextweek:bool=True, 
        dict_output:bool=False 
    ) -> None | dict:

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = datetime.now().date()
    temp_result = defaultdict(list)
    result = defaultdict(list)
    
    # includes current weekends and Monday-Friday nextweek
    if nextweek: 
        next_monday = today + timedelta(days=-today.weekday(), weeks=1)
        max_date = next_monday + timedelta(days=4) # next_friday
        min_date = next_monday - timedelta(days=2) # weekends_start
    # forward 7 days
    else:  
        min_date = today 
        max_date = min_date + timedelta(days=7)
    
    for user in users:
        if not isinstance(user["birthday"],datetime):
            print("Incorrect type \"birthday\" - not instance of datetime\n")
            continue 

        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=min_date.year)

        if  birthday_this_year < min_date or birthday_this_year > max_date:
            continue
        
        weekday_num = birthday_this_year.weekday()  
        if weekday_num in [5,6]:
            birthday_this_year = birthday_this_year + timedelta(days=(7 - birthday_this_year.weekday()))
            
        weekday_name = birthday_this_year.strftime('%A')
        temp_result[weekday_name].append(user['name'])

    if not len(temp_result):
        # print("Nobody has a birthday")
        # return 
        return f"Nobody has a birthday"

    result = { day:temp_result[day] for day in weekdays if len(temp_result[day])}

    if dict_output:
        return result
    
    if len(result):
        for key, val in result.items():
            print(f"{key}: {', '.join(val)}")
