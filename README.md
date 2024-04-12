# Kanban

A CLI Tool for maintaining kanban boards.
Can maintain projects with multiple boards and tasks.

## Installation

Clone this repository to your local machine. Navigate to KanbanFrontend and run the following command.

```
pip install .
```

Then run the Django webserver. Navigate to KanbanBackend and run:

```
python manage.py runserver
```

## Commands

Login

```
kanban login --username <username> --password <password>
```

---

Logout

```
kanban logout
```

---

Register

```
kanban register --username <username> --email <email> --password  <password>
```

---

Switch (similar to git checkout)

```
kanban switch --project <project> [and/or] --board <board>
```

---

Create

```
kanban createproject/createboard/createtask <args>
```

---

Show

```
kanban show --project/--board/--task <args>
```

---

Delete

```
kanban delete --project/--board/--task <args>
```
