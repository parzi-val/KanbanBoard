import typer
from rich.console import Console
from rich.theme import Theme
from kanban.apicalls import Session
from kanban.tools import MutuallyExclusiveGroup
import json

app = typer.Typer(no_args_is_help=True)
try:
    with open('data.json','r') as f:
        data = json.load(f)
    sessionid = data["cookie"] if "cookie" in data.keys() else None
except FileNotFoundError:
    sessionid = None

sesh = Session(sessionid)
theme = Theme({
    "error" : "bold red"
})
console = Console(theme=theme)

@app.command(help="Login command.")
def login(username:str = typer.Option(prompt=True),password:str = typer.Option(prompt=True,hide_input=True)):
    response = sesh.login(username,password)
    console.print(response.content)

@app.command(help="Logout command")
def logout():
    response = sesh.logout()
    console.print(response.content)


@app.command(help="Register new user.")
def register(username:str=typer.Option(prompt=True),
                email:str=typer.Option(prompt=True),
                password=typer.Option(prompt=True,hide_input=True)):
    response = sesh.user_registration(username,email,password)
    console.print(response.content)

@app.command(help="Switch between workspaces (projects/boards)")
def switch(project:str=typer.Option(default=None),board:str=typer.Option(default=None)):
    response = sesh.switch(project=project,board=board)
    console.print(response.content)


@app.command(help="Create new project.")
def createproject(name:str=typer.Option(prompt=True),
                    start_date:str=typer.Option(prompt=True),
                    end_date:str=typer.Option(prompt=True),
                    desc:str=typer.Option(prompt=True)):
    response = sesh.create_project(name=name,start_date=start_date,end_date=end_date,desc=desc)
    console.print(response.content)


@app.command(help="Create new board.")
def createboard(name:str=typer.Option(prompt=True)):
    response = sesh.create_board(name=name)
    console.print(response.content)


@app.command(help="Create new task.")
def createtask(name:str=typer.Option(prompt=True),
                desc:str=typer.Option(prompt=True),
                assigned:str=typer.Option(prompt=True),
                reporter:str=typer.Option(prompt=True)):
    response = sesh.create_task(name=name,desc=desc,assigned=assigned,reporter=reporter)
    console.print(response.content)


exclusivity_callback = MutuallyExclusiveGroup()

@app.command(help="Delete project/board/task.")
def delete(project:str=typer.Option(None,callback=exclusivity_callback),
            board:str=typer.Option(None,callback=exclusivity_callback),
            task:str=typer.Option(None,callback=exclusivity_callback)):
    if project:
        response = sesh.delete_project(project)
    elif board:
        response = sesh.delete_board(board)
    elif task:
        response = sesh.delete_task(task)

    console.print(response.content)


@app.command(help="Show project/board/task info.")
def show(project:str=typer.Option(None,callback=exclusivity_callback),
            board: bool = typer.Option(False, "--board"),
            task:str=typer.Option(None,callback=exclusivity_callback)):
    if project:
        response = sesh.show_project(project)
    if board:
        response = sesh.show_board()
    if task:
        response = sesh.show_task(task)

    console.print(response.content)

@app.command(help="Change status of task.")
def setstatus(task:str=typer.Option(None)):
    response = sesh.set_status(task)
    console.print(response.content)

@app.command(help="Show current workspace.")
def status():
    response = sesh.status()
    console.print(response.content)

@app.command(help="Show assigned tasks.")
def tasks():
    response = sesh.show_assigned_task()
    console.print(response.content)    

if __name__ == "__main__":
    app()