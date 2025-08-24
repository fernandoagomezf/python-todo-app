# python-todo-app

A command-line application written in Python to manage to-do tasks. This is part
of my python learning journey. 

## Functional specifications

The application uses command-line to issue instructions. Overall, the application has the 
following features:
* Add, edit, delete a new task
* View existing tasks in a simple grid view.
* Track progress of a task (from 0% to 100%).
* Promote or demote the priority of a task.
* Automatic status management: 0% - Pending, 100% - Completed, anywhere in between In progress.
* Color-coded task indicators.

## Technical specifications

### Dependencies

The application was built with Python 3.13 in mind. It uses the following packages:
* sqlite3 - to persist the data in a local database file "todo.db". 
* pandas - for loading and saving the data, using a DataFrame for data manipulation. 
* tabulate - shows a grid in the console terminal.
* colorama - used for color-coding characters in the grid view.

**Install dependencies**:

    pip install pandas sqlite3 tabulate colorama

**Run the application**:
    
    python main.py

### Database

The application stores all the data into a local sqlite3 database file called "todo.db". The data is loaded/saved using DataFrame in-built methods, and the data is overwritten with every save. Since this is a small project, no further optimization is needed. The database will be created using the following schema.

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

If the data file is not found, it will be recreated. 

## Architecture

The application will be a command-line application, no user 
interface will be added other than the terminal. Possible commands:

* show - displays the tasks availble, including an icon telling whether the task is overdue or not.
* add - adds a new task, input the subject, due date and notes.
* edit - allows to edit a specific task by changing the subject, due date and notes.
* delete - removes an existing task.
* detail - shows the detail of a specific task, including the notes.
* progress - allows to report a change in the progress of ta task, use 0 to mark the task as pending, 100 to mark it as completed.
* promote - changes the priority of a task, from low to normal, or normal to high.
* demote - changes the priority of atask, from normal to low, or high to normal.

Other commands for application management:
* help - shows a small menu of the available commands.
* clear - clears the screen.
* exit - terminates the application.

The data will be persisted in a SQLite 3 local database. Internally, the data is loaded 
when the application starts into a Pandas DataFrame, and saved as a table when a 
modification is made (e.g. a new task is added or edited).


## Change log

v0.1 First version with all code in one file, only using functions. Hopefully in 
the future I'll add classes and a more structured approach, for now it was a 
very simple exercise to familiarize myself with parts of the language. 