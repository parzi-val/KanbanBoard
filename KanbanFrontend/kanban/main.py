import typer
from rich.console import Console
from rich.theme import Theme
from kanban.apicalls import Session,erred
from kanban.tools import MutuallyExclusiveGroup,Tables
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
    console.print(sesh.login(username,password)[0])

@app.command(help="Logout command")
def logout():
    response = sesh.logout()
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])

@app.command(help="Register new user.")
def register(username:str=typer.Option(prompt=True),
                email:str=typer.Option(prompt=True),
                password=typer.Option(prompt=True,hide_input=True)):
    response = sesh.user_registration(username,email,password)
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])

@app.command(help="Switch between workspaces (projects/boards)")
def switch(project:str=typer.Option(default=None),board:str=typer.Option(default=None)):
    response = sesh.switch(project=project,board=board)
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])

@app.command(help="Create new project.")
def createproject(name:str=typer.Option(prompt=True),
                    start_date:str=typer.Option(prompt=True),
                    end_date:str=typer.Option(prompt=True),
                    desc:str=typer.Option(prompt=True)):
    response = sesh.create_project(name=name,start_date=start_date,end_date=end_date,desc=desc)
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])

@app.command(help="Create new board.")
def createboard(name:str=typer.Option(prompt=True)):
    response = sesh.create_board(name=name)
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])


@app.command(help="Create new task.")
def createtask(name:str=typer.Option(prompt=True),
                desc:str=typer.Option(prompt=True),
                assigned:str=typer.Option(prompt=True),
                reporter:str=typer.Option(prompt=True)):
    response = sesh.create_task(name=name,desc=desc,assigned=assigned,reporter=reporter)
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])

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
    if response[1] == -1  :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])
@app.command(help="Show project/board/task info.")
def show(project:str=typer.Option(None,callback=exclusivity_callback),
            board: bool = typer.Option(False, "--board"),
            task:str=typer.Option(None,callback=exclusivity_callback)):
    if project:
        response = sesh.show_project(project)
        if response[1] == -1  :
            console.print(erred(response[0]))
        elif response[1] == 1:
            console.print(response[0])
        else:
            console.print(Tables.prjfmt(response[0]))
    if board:
        response = sesh.show_board()
        if response[1] == -1  :
            console.print(erred(response[0]))
        elif response[1] == 1:
            console.print(response[0])
        else:        
            console.print(Tables.brdfmt(response[0]))
    if task:
        response = sesh.show_task(task)
        if response[1] == -1   :
            console.print(erred(response[0]))
        elif response[1] == 1:
            console.print(response[0])
        else:
            console.print("\n",Tables.taskfmt(response[0]))

@app.command(help="Change status of task.")
def setstatus(task:str=typer.Option(None)):
    response = sesh.set_status(task)
    if response[1] == -1   :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(response[0])

@app.command(help="Show current workspace.")
def status():
    response = sesh.status()
    if response[1] == -1   :
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(Tables.currfmt(response[0]))

@app.command(help="Show assigned tasks.")
def tasks():
    response = sesh.show_assigned_task()
    if response[1] == -1   :     
        console.print(erred(response[0]))
    elif response[1] == 1:
        console.print(response[0])
    else:
        console.print(Tables.assgfmt(response[0]))      

if __name__ == "__main__":
    app()