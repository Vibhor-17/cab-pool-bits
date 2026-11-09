# cab-pool-bits
# SUTT Backend Task 1 - Cab Pool Matcher

This is my submission for the SUTT Backend Recruitment Task 1. It is a CLI-based cab pool matcher built in Python for managing the end-of-semester cab rush to Delhi and Jaipur.

## Important things to consider before running
* **Python Version:** Please run this using **Python 3.12 or above** (since I have used nested quotes inside f-strings for formatting passenger lists).
* **External Package:** I used `tabulate` to print the cabs and waiting queues cleanly as tables in the terminal.
* **`state.json` Handling:** Please **do not manually edit or pre-create `state.json`**. The app automatically generates `state.json` from `cabs.json` on the first run and updates it after every task. If `state.json` is missing or gets corrupted, the startup check catches it and creates a fresh `state.json` from `cabs.json`. That is why it is important to not corrupt the `state.json` during the program/app is running,( for testing purposes the afforsaid error handling works).


## How `cabs.json` is Structured
`cabs.json` is completely customizable. You can add or edit the initial cabs before starting a fresh run:
```json
[
  {
    "driver": "Mohan Kumar",
    "seats": 4,
    "destination": "Delhi",
    "time_slot": "Morning"
  }
]
```
When the app runs for the first time, it reads `cabs.json` and adds two extra fields to each cab dictionary inside `state.json`: `"has_left": False` and `"passengers": []`.
* a sample cabs.json is also provided.
---

## How My Code & Sorting Logic Work Across Tasks

I created two classes (`RideRequest` and `Cab`) for Phase 1 and used `state.json` (loaded into the `data2` dictionary) to keep track of `"cabs"` and `"waiting_queues"`. Each trip slot key is stored in the format `"{destination} and {time_slot}"` (for example, `"Delhi and Morning"`) via the `slot()` method in the `Cab` class.
* <I have used `task_number` to say  the menu option that the user has chosen to be exercised, I also created `task_1() task_3() task_4()` functions inside the code>

### Task 1 (`task_1`): Adding a New Ride Request
* Takes user input for first name, destination (`1-2` or name via `dest_dict`), time slot (`1-4` or name via `timeslot_dict`), and year (`1-5`) with `while True` validation loops so wrong inputs don't crash the program.
* The user is given the liberty to write their name without caring much about capitalisation as that is taken care by `.title()`. So is the case with destination name and time slot but the user can also choose the serial number and avoid typing entire name afterall for this feasiblity I used two separate dictionaries. 
* Captures the exact request time using `datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")`.
* Creates a `RideRequest` object, converts it into a dictionary using `.to_dict()`, and appends it to the list for that specific trip key (`f"{destination} and {time_slot}"`) inside `data2["waiting_queues"]`.
* Immediately saves the updated `data2` back into `state.json`.To avoid any loss of data if the program is interruped by any chance.

### Task 2 (`task_number == 2`): Viewing Waiting Queues and All Cabs
* Reads `state.json` and loops through `data2["cabs"]`.
* Formats each cab's passenger list into `"Name(Yr-X)"` and updates the `"seats"` display to show how many seats are taken out of the total capacity (like `"3/4"`).
* Prints both the cabs table and each slot's waiting queue list using `tabulate`.

### Task 3 (`task_3`): Previewing Cab Matches (How the List & Sorting Work)
* Since Task 3 is **only a preview**, it does not modify `state.json`.
* It loops through all cabs in fixed order. For each open cab (`objectt.has_left == False`), it pulls the waiting list for that cab's slot (`objectt.slot()`) and sorts it using Python's `sorted()` with a custom lambda key:
  ```python
  key=lambda x: (-x["year"], x["submitted_at"])
  ```
  * `-x["year"]` makes higher years negative (`-5` comes before `-4`), cause it was demanded that seniors are given higher priority<I haven't used heap in this option as this is only a preview, although it is used in later option> .
  * `x["submitted_at"]` breaks ties for same-year students by putting the earlier timestamp first.
* **Why I used `already_previewed = set()`:** If there are multiple open cabs for the same trip (like two cabs for `"Delhi and Morning"`), the first cab previews the top seniors up to its seat limit and adds their `(name, year, submitted_at)` tuple into `already_previewed`. When the loop checks fot the second cab for the same slot, the list comprehension filters out students already in `already_previewed` so the second cab previews the *next* students in line instead of showing the same students twice.

### Task 4 (`task_4`): Dispatching a Cab (How the `heapq` Works)
* Asks the user for the destination and time slot to dispatch.
* Loops through `data2["cabs"]` to find the first open cab matching `f"{destination} and {time_slot}"` where `has_left == False`.
* Once found, it creates an empty min-heap (`heap = []`) and pushes every waiting student for that slot into `heapq` using `enumerate`< first i was trying to use index as a parameter to decide the priority also as the submitted time could also be same; but I later on added a millisecond option to avoid this>:
  ```python
  heapq.heappush(heap, (-student["year"], student["submitted_at"], idx, student))
  ```
* **How the Heap Tuple Works:**
  1. `-student["year"]`: Since `heapq` is a min-heap, negating the year makes 5th years (`-5`) pop before 1st years (`-1`).
  2. `student["submitted_at"]`: If two students are in the same year, the earlier timestamp string is smaller, so whoever requested first pops first.
  (3. `idx`: The list index from `enumerate`. If two students from the same year ever have the exact same timestamp down to the second, `idx` acts as a tie-breaker based on who was appended to the list first, preventing Python from crashing by trying to compare two `student` dictionaries directly.){lateer this was avoided by millisecond consideration}
  4. `student`: The actual student dictionary at index `[3]`.
* It then runs a `for` loop for the number of available seats (`objectt.seats - len(objectt.passengers)`), pops the highest-priority student using `heapq.heappop(heap)[3]`, appends them to `objectt.passengers`, and removes them from `data2["waiting_queues"][objectt.slot()]`.
* Finally, it sets `"has_left": True` and saves the updated state to `state.json`.{auto saved and it re state to not to change the state.json during the program is running}

---

## Questions
---

## Why JSON Instead of Pickle?
`pickle` would have used binary as it is a binary only and there would also have been some security issues when loading untrusted files. I used **JSON** (`cabs.json` and `state.json`)  because JSON is human readable and anyone checking the project can open `state.json` directly in VS Code or any editor to see who is in the waiting queues and which cabs have left.

---

## Tricky Situations & Edge Cases

1. **Half-Empty Cab:**
   In `task_4()` <this option deals with the "dispatch part">, the loop pops from `heap` only while `len(heap) > 0`(condition is specificaaly mentioned). If a 4-seater cab is dispatched when only 1 or 2 students are waiting, it pops those 1 or 2 students, adds them to `passengers`, marks `"has_left": True`, and sends the cab off. If 0 students are waiting (`len(people) == 0`), the app prints a message that the cab cannot leave with no passengers and doesn't mark it as left.

3. **No Cabs Left:**
   Because `task_1()` directly appends new requests to `data2["waiting_queues"]` in `state.json` without the neeed of an open cab right , students who submit requests after all cabs have left are still saved in the waiting queue and show up in Task 2. If someone tries to dispatch a cab for that trip in `task_4()`, the loop finishes and prints `"No open cabs available for this trip."`.

4. **Same Year Students:**
   Handled by both `submitted_at` and `idx` in the heap tuple `(-student["year"], student["submitted_at"], idx, student)` in `task_4()`, and by `(-x["year"], x["submitted_at"])` in `task_3()` but the `idx` handling is not really required as the submitted time is taken upto milliseconds which is almost impossilbe to make same except if the user delibrately changes it in `state.json`. Since `task_1()` appends requests in the order they arrive and saves them to `state.json`, the exact arrival order is kept even if the app is closed and reopened.

5. **Lots of Students (Big-O Complexity for N = 1,000 requests):**
   * **Adding 1 request & adding all 1,000:**
     * In `task_1()`, appending 1 request to the waiting queue list in memory takes **O(1)**, so adding 1,000 requests takes **O(N)** (excluding JSON file read/write).
     * When pushing into the `heapq` priority queue in `task_4()`, pushing 1 request with `heappush` takes **O(\log N)**, and pushing all 1,000 requests into the heap takes **O(N \log N)**.
   * **Sending off 1 cab (picking up to 4 students):**
     *Once the heap is built (\(O(N \log N)\)), popping up to 4 students with `heappop` takes \(4 \times O(\log N) = O(\log N)\) time, and removing those 4 students from the waiting list with `.remove()` takes 4 × O(N) = O(N) time.
   * **Finding an open cab for a trip:**
     * **O(C)**, where C is the total number of cabs in `cabs.json`. In `task_4()`, the code loops through `data2["cabs"]` one by one until it finds the first cab matching the trip slot with `has_left == False`, which does not depend on the number of waiting students N.
