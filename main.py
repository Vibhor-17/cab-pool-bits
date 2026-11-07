
import json
from datetime import datetime
from tabulate import tabulate

# start of basic cli interface
print("====================================================")
print("                Cab Pool (BITS PILANI)              ")
print("====================================================")

#load the json file
print("loading json file")
try:  
    with open("cabs.json","r", encoding="utf-8") as f:
        data = json.load(f)
        # print(data)
    print("cab.json file loaded successfully.")
except FileNotFoundError: 
    print(f"Error: The file 'cabs.json' was not found.")
except PermissionError:
    print(f"Error: You do not have permission to access 'cabs.json'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


from pathlib import Path
state_path = Path("state.json")
print("enquiring if state.json already exist")
if state_path.exists():
    print("state.json already exist,(app not running for the first time)")
    # data2 ={}          #use data2 variable ahead for data in state.json global variable
else:
    print("state.json doesn't exist\n creating state.json for optimising and memory purposes")
    with open("state.json", "w", encoding='utf-8') as f2:
        data2 = {"cabs":[], "waiting_queues" : {}}
        for cab in data:
            cab["has_left"] = False
            cab["passengers"] = []
            data2["cabs"].append(cab) 
        json.dump(data2,f2,indent= 4)
    print("state.json file created, program ready for getting ride requests")


print("choose a task (1-5)")
print("1. Add a new ride request.")
print("2. See everyone still waiting, plus all cabs (both open and already left).")
print("3. preview cab matches")
print("4. Dispatch Cab") 
print("5. Quit the app.\n\n")



# def open_state():
#     with open("state.json",'r',encoding="utf-8") as f:
#         data2 = json.load(f)

    

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

    def priority(self,other):
        return (self.year,self.submitted_at) 




class Cab:
    '''sample object
    cab1 = Cab(
    driver="Ramesh Kumar",
    seats=4,
    destination="Delhi",
    time_slot="Morning"
    hasleft
    passengers
    )
'''
    def __init__(self,driver,seats,destination,time_slot,has_left,passengers):
        self.driver = driver
        self.seats = seats
        self.destination =destination
        self.time_slot =time_slot
        self.has_left = has_left
        self.passengers = passengers

    def slot(self):
        return(f"{self.destination} and {self.time_slot}")






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
    key = f'{destination} and {time_slot}'
    if key not in data2['waiting_queues']:
        data2['waiting_queues'][key] = []
    data2['waiting_queues'][key].append(request.to_dict())

    with open("state.json",'w',encoding='utf-8') as f:
        json.dump(data2,f ,indent = 4)
        

def task_3():
    with open("state.json",'r',encoding="utf-8") as f:
        data2 = json.load(f)
    # cab_objests = {}
    already_previewed = set() 
    for cab in data2['cabs']:
        # print(tabulate([cab],headers="keys"))
        objectt = Cab(driver=cab["driver"],seats=cab["seats"],destination = cab["destination"],time_slot=cab["time_slot"],has_left = cab["has_left"],passengers=cab["passengers"])
        
        if objectt.has_left == True:
            pass
        else:
            if objectt.seats == len(objectt.passengers):
                cab2 = {**cab, "has_left": True}
                # print(tabulate([cab2],headers="keys"))
                p_names = ", ".join([f"{p['name']} (Yr {p['year']})" for p in cab2.get("passengers", [])])
                display_row = [{
                    "Driver": cab2["driver"],
                    "Trip": objectt.slot(),
                    "Seats": f"{len(cab2.get('passengers', []))}/{cab2['seats']}",
                    "Status": "Departed (Full)",
                    "Previewed Passengers": p_names if p_names else "None"
                }]
                print(tabulate(display_row, headers="keys", tablefmt="grid"))
                print()
            
            else:  
                if objectt.slot() not in data2["waiting_queues"]:
                    data2["waiting_queues"][objectt.slot()] = []
                # students = [s for s in 
                #     sorted(
                #     data2["waiting_queues"][objectt.slot()],
                #     key =lambda x: (-x["year"],x["submitted_at"]) )
                #     if s not in already_previewed]   
                students = [
                    s for s in sorted(
                        data2["waiting_queues"][objectt.slot()],
                        key=lambda x: (-x["year"], x["submitted_at"])
                    ) if s["name"] not in already_previewed
                ]
                
                preview = objectt.passengers    
                for i in range(objectt.seats - len(objectt.passengers)):

                    if i < len(students):
                        preview.append(students[i])
                        already_previewed.add(students[i]["name"])
                cab2 = {**cab, "has_left": True, "passengers": preview}
                # print(tabulate(cab2,headers="keys"))
                p_names = ", ".join([f"{p['name']} (Yr {p['year']})" for p in preview])
                display_row = [{
                    "Driver": cab2["driver"],
                    "Trip": objectt.slot(),
                    "Seats": f"{len(preview)}/{cab2['seats']}",
                    "Status": "Previewed Departure",
                    "Previewed Passengers": p_names if p_names else "None"
                }]
                print(tabulate(display_row, headers="keys", tablefmt="grid"))
                print()
                                
                

        
    

    



def task():
    expected_task_no = [1, 2, 3, 4, 5]

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

    elif task_number == 2:
        with open("state.json",'r',encoding="utf-8") as f:
            data2 = json.load(f)
        print(tabulate(data2["cabs"],headers="keys"))
        print()
        if data2["waiting_queues"] == {}:
            print("no one in waiting queues")
        else:
            for slot in data2["waiting_queues"]:
                print(f"            {slot}            ")
                print(tabulate(data2['waiting_queues'][slot],headers="keys"))
                print()

    elif task_number == 3:
        task_3()

    elif task_number == 4:
        print()

    else:
        print("quitting app. thanks")
        return False
    return True



while task():
    pass

