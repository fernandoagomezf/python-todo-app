
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

app_title = "ToDo App v0.1"
cnnstr = "todo.db"
priority_low = 0
priority_normal = 1
priority_high = 2
status_pending = 0
status_inprocess = 1
status_completed = 2

data:pd.DataFrame = None

def load_data() -> pd.DataFrame:
    global data
    with sql.connect(cnnstr) as cnn:
        try:
            data = pd.read_sql("select * from tasks", cnn, )
        except pd.errors.DatabaseError:
            data = pd.DataFrame({
                'id': pd.Series(dtype='str'),
                'code': pd.Series(dtype='str'),
                'subject': pd.Series(dtype='str'),
                'due_date': pd.Series(dtype='datetime64[ns]'),
                'status': pd.Series(dtype='str'),
                'priority': pd.Series(dtype='str'),
                'progress': pd.Series(dtype='float'),
                'notes': pd.Series(dtype='str')
            })
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
    sys.exit(0)

def task_icon(row):
    icon = ""
    progress = int(row["progress"])

    if progress >= 1.0:
        icon = f"{Fore.GREEN}✓{Fore.RESET}"
    else:
        due_date = pd.to_datetime(row["due_date"]).date()
        today = datetime.now().date()
        if due_date == today:
            icon = f"{Fore.YELLOW}!{Fore.RESET}"
        elif (due_date < today):
            icon = f"{Fore.RED}✗{Fore.RESET}"

    return icon

def task_status(value):
    match value:
        case 0: return "Pending"
        case 1: return "In Process"
        case 2: return "Completed"
        case _: return "Cancelled"

def cmd_show():
    global data

    clrscr()

    view = data.copy()
    view = view.drop(columns=["id", "notes"])
    view.insert(0, "", view.apply(task_icon, axis=1))
    view["status"] = view["status"].apply(task_status)
    view["progress"] = view["progress"].apply(lambda x: f"{x:.0%}")
    view["priority"] = view["priority"].apply(lambda x: "Low" if x == 0 else "Normal" if x == 1 else "High")
    view = view.rename(columns={
        "code": "Code",
        "subject": "Subject",
        "due_date": "Due Date",
        "status": "Status",
        "priority": "Priority",
        "progress": "Progress"
    })

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

def input_date(field_name:str) -> str:
    value = ""
    while True:
        value = input(f"\t{field_name}: ")
        if is_valid_date(value):
            break
        print(f"\t** The field must be a valid date in the format yyyy-mm-dd **")
    return value

def is_valid_str(value:str, minlen=1, maxlen=250) -> bool:
    pattern = rf"^.{{{minlen},{maxlen}}}$"
    ismatch = re.fullmatch(pattern, value)
    return bool(ismatch)

def input_str(field_name:str, mandatory=True, maxlen=250) -> str:
    value = ""
    minlen = 1 if mandatory else 0
    while True:
        value = input(f"\t{field_name}: ")
        if is_valid_str(value, minlen, maxlen):
            break
        print(f"\t** The field must have at least {minlen} characters and at most {maxlen} **")
    return value

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

def get_commands():
    return {
        "help": (cmd_help, "Shows available application commands."),
        "exit": (cmd_exit, "Terminates the application."),
        "show": (cmd_show, "Displays the tasks available."),
        "add": (cmd_add, "Adds a new task, will require further input.")
    }

def run():
    print(f"===== {app_title} =====")

    colorama.init()
    load_data()
    cmd_show()

    commands = get_commands()
    while (True):
        print("Input a command or type help")
        cmd_input = input(":> ")
        if cmd_input in commands:
            cmd, _ = commands[cmd_input]
            cmd()
        else:
            print("Command not recongized.")


if __name__ == "__main__":
    run()
