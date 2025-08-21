
import base64
import colorama
import datetime
import os
import sys
import pandas as pd
import re
import sqlite3 as sql
import tabulate as tab
import uuid

from colorama import Fore
from datetime import datetime
from typing import Tuple

app_title = "ToDo App v0.1"
cnnstr = "todo.db"
priority_low = 0
priority_normal = 1
priority_high = 2
status_pending = 0
status_inprocess = 1
status_completed = 2

data:pd.DataFrame

def load_data() -> pd.DataFrame:
    global data     
    with sql.connect(cnnstr) as cnn:
        try:
            data = pd.read_sql("select * from tasks", cnn)
        except pd.errors.DatabaseError:
            data = pd.DataFrame({
                'id': pd.Series(dtype='str'),
                'code': pd.Series(dtype='str'),
                'subject': pd.Series(dtype='str'),
                'due_date': pd.Series(dtype='datetime64[ns]'),
                'status': pd.Series(dtype='int'),  
                'priority': pd.Series(dtype='int'), 
                'progress': pd.Series(dtype='float'),
                'notes': pd.Series(dtype='str')
            })
            cnn.execute("""
                CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    code TEXT,
                    subject TEXT,
                    due_date TEXT,
                    status INTEGER,
                    priority INTEGER,
                    progress REAL,
                    notes TEXT
                )
            """)
        return data

def save_tasks():
    with (sql.connect(cnnstr) as cnn):
        global data
        data.to_sql("tasks", cnn, index=False, if_exists="replace")

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def cmd_exit():
    clrscr()
    sys.exit(0)

def task_icon(row) -> str:
    icon = ""
    progress = float(row["progress"]) 

    if progress >= 1.0:
        icon = f"{Fore.GREEN}✓{Fore.RESET}"
    else:
        due_date = pd.to_datetime(row["due_date"]).date()
        today = datetime.now().date()
        if due_date == today:
            icon = f"{Fore.YELLOW}!{Fore.RESET}"
        elif due_date < today:
            icon = f"{Fore.RED}✗{Fore.RESET}"

    return icon

def task_status(value):
    match value:
        case 0: return "Pending"
        case 1: return "In Process"
        case 2: return "Completed"
        case _: return "Cancelled"

def get_view(rename_cols=True, drop_extra_cols=True):
    global data

    view = data.copy()
    if drop_extra_cols:
        view = view.drop(columns=["id", "notes"])

    if len(view) == 0: # the dataframe is empty
        view[""] = pd.Series(dtype='object')
        view["status"] = pd.Series(dtype='object')
        view["progress"] = pd.Series(dtype='object')
        view["priority"] = pd.Series(dtype='object')
    else:
        icon_result = view.apply(task_icon, axis=1)    
        view.insert(0, "", icon_result)
        view["status"] = view["status"].apply(task_status)
        view["progress"] = view["progress"].apply(lambda x: f"{x:.0%}")
        view["priority"] = view["priority"].apply(lambda x: "Low" if x == 0 else "Normal" if x == 1 else "High")
    
    if rename_cols:
        view = view.rename(columns={
            "code": "Code",
            "subject": "Subject",
            "due_date": "Due Date",
            "status": "Status",
            "priority": "Priority",
            "progress": "Progress",
        })

    return view

def cmd_show():
    global data

    clrscr()
    view = get_view()
    count = len(view)
    print(f"Found {count} task{'s' if count != 1 else ''}.")
    result = tab.tabulate(view, headers="keys", tablefmt="psql", showindex=False)
    print(result)

def is_valid_date(value:str) -> bool:
    try:
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        ismatch = re.fullmatch(pattern, value)
        if ismatch:
            datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        ismatch = False
    return ismatch

def input_date(field_name:str, mandatory:bool=True) -> str:
    while True:
        value = input(f"\t{field_name}: ")
        if not mandatory and (value is None or len(value) <= 0):
            return str()
        if is_valid_date(value):
            break
        print(f"\t** The field must be a valid date in the format yyyy-mm-dd **")
    return value

def is_valid_str(value:str, minlen=1, maxlen=250) -> bool:
    pattern = rf"^.{{{minlen},{maxlen}}}$"
    ismatch = re.fullmatch(pattern, value)
    return bool(ismatch)

def input_str(field_name:str, mandatory=True, maxlen=250) -> str:
    minlen = 1 if mandatory else 0
    while True:
        value = input(f"\t{field_name}: ")
        if is_valid_str(value, minlen, maxlen):
            break
        print(f"\t** The field must have at least {minlen} characters and at most {maxlen} **")
    return value

def input_task_code():
    while True:
        value = input(f"\tTask Code: ")
        if is_valid_str(value, 6, 6):
            break
        print(f"\t** The task code is mandatory and has to be 6 characters long **")
    return value.upper()

def is_valid_range(value:str, min_range:int, max_range:int) -> bool:
    if not value.isdigit():
        return False

    num = int(value)
    return min_range <= num <= max_range

def input_number(field_name:str, range_value:Tuple[int, int]) -> int:
    min_range, max_range = range_value
    while True:
        value = input(f"\t{field_name}: ")
        if is_valid_range(value, min_range, max_range):
            break

        print(f"\t** The field must be a valid number between {min_range} and {max_range}")
    return int(value)

def cmd_add():
    global data
    clrscr()

    print(f"Inserting a new task, please provide the following data:")

    subject = input_str("Subject", True)
    due_date = input_date("Due Date")
    notes = input_str("Notes", False, 5000)
    code = base64.b32encode(uuid.uuid4().bytes)[:6].decode('ascii')

    data.loc[len(data)] = {
        "id": str(uuid.uuid4()),
        "code": code,
        "subject": subject,
        "due_date": due_date,
        "status": status_pending,
        "priority": priority_normal,
        "progress": 0,
        "notes": notes
    }
    save_tasks()

    clrscr()
    cmd_show()

def cmd_help():
    clrscr()
    print("Available commands:")
    for name, (cmd, txt) in get_commands().items():
        print(f"* {name} - {txt}")

def cmd_clear():
    clrscr()

def cmd_detail():
    global data
    code = input_task_code()
    view = get_view(False, False)
    row = view.loc[view["code"] == code]
    if not row.empty:
        item = row.iloc[0]
        print(f"\t* Code:\t\t{item["code"]}")
        print(f"\t* Subject:\t{item["subject"]}")
        print(f"\t* Due Date:\t{item["due_date"]}")
        print(f"\t* Status:\t{item["status"]}")
        print(f"\t* Priority:\t{item["priority"]}")
        print(f"\t* Progress:\t{item["progress"]}")
        print(f"\t* Notes:\t{item["notes"]}")
    else:
        print(f"\t** task with code {code} not found.")


def cmd_edit():
    global data
    code = input_task_code()
    view = get_view(False, False)
    row = view.loc[view["code"] == code]
    if not row.empty:
        item = row.iloc[0]
        print(f"\tEnter the new values.")

        print(f"\t* Subject:\t{item["subject"]}")
        subject = input_str("Subject", False)
        if subject is None or len(subject) <= 0:
            subject = item["subject"]
        print(f"\t* Due Date:\t{item["due_date"]}")
        due_date = input_date("Due Date", False)
        if due_date is None or len(due_date) <= 0:
            due_date = item["due_date"]
        print(f"\t* Notes:\t{item["notes"]}")
        notes = input_str("Notes", False, 5000)
        if notes is None or len(notes) <= 0:
            notes = item["notes"]

        cols = ["subject", "due_date", "notes"]
        vals = [subject, due_date, notes]
        data.loc[data["code"] == code, cols] = vals
        save_tasks()

        clrscr()
        cmd_show()
    else:
        print(f"\t** task with code {code} not found.")

def cmd_delete():
    global data
    code = input_task_code()
    row = data[data["code"] == code]
    if row.index >= 0:
        data = data.drop(row.index)
        save_tasks()
        cmd_show()
    else:
        print(f"\t** task with code {code} not found.")

def cmd_progress():
    global data
    code = input_task_code()

    if not data[data["code"] == code].empty:
        progress = float(input_number("Progress", (0, 100)))
        progress = round(progress / 100.0, 2)
        data.loc[data["code"] == code, "progress"] = progress
        data.loc[data["code"] == code, "status"] = 0 if progress <= 0.0 else 2 if progress >= 1.0 else 1

        save_tasks()
        cmd_show()
    else:
        print(f"\t** task with code {code} not found.")

def cmd_promote():
    global data
    code = input_task_code()

    row = data.index[data["code"] == code]
    if not row.empty:
        priority = data.at[row[0], "priority"]
        data.at[row[0], "priority"] = min(priority + 1, 2)

        save_tasks()
        cmd_show()
    else:
        print(f"\t** task with code {code} not found.")

def cmd_demote():
    global data
    code = input_task_code()

    row = data.index[data["code"] == code]
    if not row.empty:
        priority = data.at[row[0], "priority"]
        data.at[row[0], "priority"] = max(priority - 1, 0)

        save_tasks()
        cmd_show()
    else:
        print(f"\t** task with code {code} not found.")

def get_commands():
    return {
        "add": (cmd_add, "Adds a new task, will require further input."),
        "clear": (cmd_clear, "Clears the content of the screen."),
        "delete": (cmd_delete, "Deletes a specific task from the list."),
        "demote": (cmd_demote, "Decreases the priority of a task."),
        "detail": (cmd_detail, "Shows the details of a specific task."),
        "edit": (cmd_edit, "Allows you to change the details of a task."),
        "exit": (cmd_exit, "Terminates the application."),
        "help": (cmd_help, "Shows available application commands."),
        "progress": (cmd_progress, "Reports the advancement of a task."),
        "promote" : (cmd_promote, "Increases the priority of a task."),
        "show": (cmd_show, "Displays the tasks available."),
    }

def run():
    print(f"===== {app_title} =====")

    colorama.init()
    load_data()
    cmd_show()

    commands = get_commands()
    while True:
        print("Input a command or type help")
        cmd_input = input(":> ")
        if cmd_input in commands:
            cmd, _ = commands[cmd_input]
            cmd()
        else:
            print("Command not recongized.")


if __name__ == "__main__":
    run()
