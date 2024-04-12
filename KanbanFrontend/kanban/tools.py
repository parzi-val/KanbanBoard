from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from rich.columns import Columns
from rich.text import Text
import typer
from enum import Enum



def MutuallyExclusiveGroup():
    group = set()
    def callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
        # Add cli option to group if it was called with a value
        if value is not None and param.name not in group:
            group.add(param.name)
        if len(group) > 1:
            raise typer.BadParameter(f"{", ".join(list(group))} are mutually exclusive.")
        return value
    return callback

class Formats(Enum):
    PROJECT = "project"
    BOARD = "board"
    TASK = "task"
    TASKS = "tasks"
    CWS = "cws"
    ERRED = "erred"
    VALID = "valid"
    DEFAULT = "default"

class Response:
    def __init__(self,content,*,fmt:Formats = Formats.DEFAULT):
        self.formats = {
            Formats.PROJECT : self.projectfmt,
            Formats.BOARD : self.boardfmt,
            Formats.TASK : self.taskfmt,
            Formats.TASKS : self.assgtasksfmt,
            Formats.CWS : self.cwsfmt,
            Formats.ERRED : self.erred,
            Formats.VALID : self.valid,
            Formats.DEFAULT : lambda x : x
        }

        self.content = self.formats[fmt](content)
        
    
    def fulfill(self,col,maxlen):
        return col + ["" for i in range(maxlen-len(col))]

    def sort(self,todo_list):
        priority_values = {"high": 3, "medium": 2, "low": 1}
        def priority_sort_key(item):
            priority = item.get("priority", "low")
            priority_num = priority_values.get(priority, 0)
            return priority_num
        sorted_todo_list = sorted(todo_list, key=priority_sort_key, reverse=True)
        return sorted_todo_list
    
    def erred(self,text):
        text = Text(text)
        text.stylize("bold red")
        return text
    
    def valid(self,text):
        text = Text(text)
        text.stylize("bold green")
        return text

    def projectfmt(self,project):
        data = [f"[green bold]{k.capitalize()}:[/green bold] [blue]{v}[/blue]" for k,v in project.items() if k not in ["Name","Boards"]]
        data += [f"[green bold]Boards:[/green bold] [blue]{", ".join(project["Boards"])}[/blue]"]
        panel = Panel(
            "\n".join(data),
            title=f"Project {project["Name"]}",
            border_style="red",
            title_align="left",
            width=50
        )
        return panel
    
    def boardfmt(self,board):
        sortedtodo = self.sort(board["todo"])
        sortedinp = self.sort(board["inprogress"])
        sorteddone = self.sort(board["done"])
        todolist = [i["name"] for i in sortedtodo]
        inplist = [i["name"] for i in sortedinp]
        donelist = [i["name"] for i in sorteddone]

        maxlen = len(max(todolist,inplist,donelist,key=len))
        todolist = self.fulfill(todolist,maxlen)
        inplist = self.fulfill(inplist,maxlen)
        donelist = self.fulfill(donelist,maxlen)
        
        todo = Panel(
            "\n".join(todolist),
            title="Todo",
            border_style="blue",
            title_align="center"
        )
        inp = Panel(
            "\n".join(inplist),
            title="In Progress",
            border_style="blue",
            title_align="center"
        )
        done = Panel(
            "\n".join(donelist),
            title="Done",
            border_style="blue",
            title_align="center"
        )
        console = Console()
        panel = Panel(
            Columns([todo,inp,done]),
            title="Kanban Board",
            border_style="green",
            title_align="left",
            padding=(1, 2),
        )
        return panel

    def taskfmt(self,task):
        data = [f"[green bold]{k.capitalize()}:[/green bold] [blue]{v}[/blue]" for k,v in task.items() if k not in ["name"]]
        panel = Panel(
            "\n".join(data),
            title=f"Task {task["name"]}",
            border_style="red",
            title_align="left",
            width=50
        )
        return panel
    
    def cwsfmt(self,cws):
        data = [f"[green bold]{k.capitalize()}:[/green bold] [blue]{v}[/blue]" for k,v in cws.items()]
        panel = Panel(
            "\n".join(data),
            title=f"Currently working on",
            border_style="red",
            title_align="left",
            width=50
        )
        return panel

    def assgtasksfmt(self,tasks):
        data = [f"[green]{i["project"]}[/green] ▷ [blue]{i["board"]}[/blue] ▷ [red]{i["name"]}[/red]" for i in tasks["tasks"]]
        panel = Panel(
            "\n".join(data),
            title ="Assigned Tasks",
            border_style="yellow",
            title_align="left",
        )

        return panel