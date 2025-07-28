
from sys import exit
from todo.application.program import TodoApp

if __name__ == "__main__":
    app = TodoApp()
    app.run()
    exit(app.return_code or 0)
