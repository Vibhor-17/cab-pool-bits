
import json
from datetime import datetime


# start of basic cli interface
print("====================================================")
print("                Cab Pool (BITS PILANI)              ")
print("====================================================")


print("choose a task (1-3)")
print("1. Add a new ride request.")
print("2. See everyone still waiting, plus all cabs (both open and already left).")
print("3. Quit the app.")
print()


#load the json file
print("loading json file")
with open("cabs.json","r", encoding="utf-8") as f:
    data = json.load(f)
    print(data)
print("json file loaded successfully")






#defining the classes #phase 1
class RideRequest:
    """  sample objecct
    req1 = RideRequest(
    name="Aarav",
    destination="Delhi",
    time_slot="Morning",
    year=5,
    submitted_at="2026-11-05 17:10:05"
    )
"""
    def __init__(self,name,destination,time_slot,year,submitted_at):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submitted_at = submitted_at

    
    def to_dict(self):
       
       return{
                "name": self.name,
                "destination": self.destination,
                "time_slot": self.time_slot,
                "year": self.year,
                "submitted_at": self.submitted_at,
                }
        
    def add_ride_request(self):
        try:
            with open("state.json", "w", encoding="utf-8") as f:
                dict = {
                "name": self.name,
                "destination": self.destination,
                "time_slot": self.time_slot,
                "year": self.year,
                "request_order": self.request_order,
                "submitted_at": self.submitted_at,
                }
                json.dump(dict, f, indent=4)
        
        except FileNotFoundError:
            print("Error: The file does not exist.")
        except PermissionError:
            print("Error: You do not have permission to access this file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")




class Cab:
    '''sample object
    cab1 = Cab(
    driver="Ramesh Kumar",
    seats=4,
    destination="Delhi",
    time_slot="Morning"
    )
'''
    def __init__(self,driver,seats,destination,time_slot):
        self.driver = driver
        self.seats = seats
        self.destination =destination
        self.time_slot =time_slot







# waiting_room = {}
#now the main program
dest_dict = {"1": "Delhi", "delhi": "Delhi", "2": "Jaipur", "jaipur": "Jaipur"}
timeslot_dict = {
    "1": "Morning", "morning": "Morning",
    "2": "Afternoon", "afternoon": "Afternoon",
    "3": "Evening", "evening": "Evening",
    "4": "Night", "night": "Night"
}


def task_1():
    name = input("enter your first name: ").strip().title()

    while True:
            print("\nDestinations: 1. Delhi | 2. Jaipur")
            raw_dest = input("Enter destination (1-2 or name): ").strip().lower()
            if raw_dest in dest_dict:
                destination = dest_dict[raw_dest]  
                break
            print(f"Sorry, we don't serve '{raw_dest}'. Please choose Delhi (1) or Jaipur (2).")
    
    while True:
            print("\nTime Slots: 1. Morning | 2. Afternoon | 3. Evening | 4. Night")
            raw_slot = input("Enter time slot (1-4 or name): ").strip().lower()
            if raw_slot in timeslot_dict:
                time_slot = timeslot_dict[raw_slot]   
                break
            print("Invalid time slot. Please choose 1-4 (Morning, Afternoon, Evening, Night).")
    while True:
            raw_year = input("\nEnter your year (1-5): ").strip()
            try:
                year = int(raw_year)
                if 1 <= year <= 5:
                    break
                print(f"Year {year} is invalid. Please enter a year between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

    tiime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    request = RideRequest(name=name, destination=destination, time_slot=time_slot, year=year,submitted_at=tiime)
    # waiting_room[f"{destination} and {time_slot}"] = request.to_dict()
    with open("state.json",'r',encoding="utf-8") as f:
        data2 = json.load(f)
    # print(request.to_dict())


    key = f'{destination} and {time_slot}'
    if key not in data2['waiting_queues']:
        data2['waiting_queues'][key] = []
    data2['waiting_queues'][key].append(request.to_dict())

    # data2['waiting_queues'][f'{destination} and {time_slot}'].append(request.to_dict())
    with open("state.json",'w',encoding='utf-8') as f:
        json.dump(data2,f ,indent = 4)
        

    





def task():
    expected_task_no = [1, 2, 3]

    while True:
        try:
            task_number = int(input("\nEnter task number (1-3): ").strip())

            if task_number not in expected_task_no:
                print("Invalid task number. Try again.")
                continue

            break

        except ValueError:
            print("Please enter a number.")




    if task_number == 1:
        task_1()
        
        task()

    elif task_number == 2:
        with open("state.json",'r', encoding='utf-8') as f:
            data2 = json.load(f)
        print(data2['waiting_queues'])
        print()
        task()


    elif task_number == 3:
        print("quitting app. thanks")


task()

