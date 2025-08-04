# python-todo-app

A command-line application written in Python to manage to-do tasks. This is part
of my python learning journey. 

## Functional specifications

The application will be able to do the 
following:
* Add a new task
* View existing tasks
* Edit existing tasks
* Report the advancement of a task
* Promote or demote the priority of a task

## Technical specifications

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