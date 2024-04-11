from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from rich.columns import Columns
import typer

def addemptyrows(col,maxlen):
        return col + ["" for i in range(maxlen-len(col))]


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


class Tables:
    @staticmethod
    def prjfmt(project):
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
    
    def sort_by_priority(todo_list):
        # Define a mapping of priority levels to numerical values
        priority_values = {"high": 3, "medium": 2, "low": 1}

        # Define a sorting key function
        def priority_sort_key(item):
            # Get the priority value from the item, default to "low" if not specified
            priority = item.get("priority", "low")
            # Map the priority to its numerical value, assume None is below low
            priority_num = priority_values.get(priority, 0)
            return priority_num
        
        sorted_todo_list = sorted(todo_list, key=priority_sort_key, reverse=True)
        return sorted_todo_list
    
    @staticmethod
    def brdfmt(board):
        todo = Tables.sort_by_priority(board["todo"])
        inp = Tables.sort_by_priority(board["inprogress"])
        done = Tables.sort_by_priority(board["done"])
        todolist = [i["name"] for i in todo]
        inplist = [i["name"] for i in inp]
        donelist = [i["name"] for i in done]
        maxlen = len(max(todolist,inplist,donelist,key=len))
        todolist = addemptyrows(todolist,maxlen)
        inplist = addemptyrows(inplist,maxlen)
        donelist = addemptyrows(donelist,maxlen)
        
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

    @staticmethod
    def taskfmt(task):
        data = [f"[green bold]{k.capitalize()}:[/green bold] [blue]{v}[/blue]" for k,v in task.items() if k not in ["name"]]
        panel = Panel(
            "\n".join(data),
            title=f"Task {task["name"]}",
            border_style="red",
            title_align="left",
            width=50
        )
        return panel
    


    
    @staticmethod
    def currfmt(current):
        data = [f"[green bold]{k.capitalize()}:[/green bold] [blue]{v}[/blue]" for k,v in current.items()]
        panel = Panel(
            "\n".join(data),
            title=f"Currently working on",
            border_style="red",
            title_align="left",
            width=50
        )
        return panel

    def assgfmt(tasks):
        data = [f"[green]{i["project"]}[/green] ▷ [blue]{i["board"]}[/blue] ▷ [red]{i["name"]}[/red]" for i in tasks["tasks"]]
        panel = Panel(
            "\n".join(data),
            title ="Assigned Tasks",
            border_style="yellow",
            title_align="left",
        )

        return panel