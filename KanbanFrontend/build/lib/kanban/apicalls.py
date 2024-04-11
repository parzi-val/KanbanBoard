import requests
import json
from rich.text import Text
from rich.console import Console

# URL to which you want to send the POST request
BASE_URL = 'http://127.0.0.1:8000/backend/'
SUFFIXES = {
    "login" : "login/",
    "logout" :"logout/",
    "register":"register/",
    "switch":"switch/",
    "show-project":"projects/get-info/",
    "show-board":"boards/get-info/",
    "show-task":"board/task/",
    "show-assigned-tasks":"tasks/",
    "create-project":"projects/create/",
    "create-board":"boards/create/",
    "create-task":"boards/add-task/",
    "delete-project":"projects/delete/",
    "delete-board":"boards/delete/",
    "delete-task":"boards/tasks/delete/",
    "set-status":"boards/tasks/status/",
    "current" : "current/"
}

def erred(text):
    text = Text(text)
    text.stylize("bold red")
    return text
def valid(text):
    text = Text(text)
    text.stylize("bold green")
    return text
console = Console()

def login_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.IS_LOGGED_IN:
            return 'Login to use this.',-1
        return func(self, *args, **kwargs)
    return wrapper

def write(data):
    with open("data.json",'w') as f:
        json.dump(data,f)
def clear():
    with open("data.json", 'w') as f:
        f.write('{}')


class Session:
    def __init__(self,session = None):
        if session:
            self.IS_LOGGED_IN = True
            self.session = session
    IS_LOGGED_IN = False
    session = None

    def headers(self):
        return {
            "Cookie":f"sessionid={self.session}"
        }
        
    def login(self,username,password):
        suffix = SUFFIXES["login"]
        data = {"username" : username,"password":password}
        response = requests.post(BASE_URL+suffix, data=json.dumps(data))

        self.session = response.cookies.get('sessionid')
        write({"cookie":self.session})
        if response.status_code == 200:
            self.IS_LOGGED_IN = True
            return valid('Logged in succesfully.'),0
            
        elif response.status_code == 400:
            return erred('Invalid username or password.'),1
    
    @login_required  
    def logout(self):
        suffix = SUFFIXES["logout"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())

        if response.status_code == 200:
            clear()
            return valid('Logged out succesfully.'),0
        
    def user_registration(self,username,email,password):
        suffix = SUFFIXES["register"]
        data = {
            "username":username,
            "email":email,
            "password":password
        }
        response = requests.post(BASE_URL+suffix,data=json.dumps(data))

        if response.status_code == 200:
            return valid('User created successfully.'),0
    
    @login_required
    def switch(self,*,project = None,board = None):
        self.CURRENT_PROJECT = project
        self.CURRENT_BOARD = board
        suffix = SUFFIXES["switch"]
        data = {key: value for key, value in [("project", project), ("board", board)] if value is not None}
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return valid(data["message"]),0
        elif response.status_code == 400:
            return erred(data["error"]),1
    
    @login_required
    def create_project(self,*,name,start_date,end_date,desc):
        suffix = SUFFIXES["create-project"]
        data = {
            "name":name,
            "start_date":start_date,
            "end_date":end_date,
            "desc":desc,
        }
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 201:
            return valid(data["message"]),0
        if response.status_code == 400:
            return erred(data["error"]),1
    
    @login_required
    def create_board(self,*,name):
        suffix = SUFFIXES["create-board"]
        data = {
            "name":name
        }
        response = requests.post(BASE_URL+suffix,data=json.dumps(data),headers=self.headers())
        data =  json.loads(response.text)
        if response.status_code == 201:
            return valid(data["message"]),0
        elif response.status_code == 400:
            return erred("Project not set. Use switch to set Project."),1
    
    @login_required
    def create_task(self,*,name,desc,assigned,reporter):
        suffix = SUFFIXES["create-task"]
        data = {
            "name" : name,
            "desc" : desc,
            "assigned" : assigned,
            "reporter" : reporter
        }        
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data =  json.loads(response.text)
        if response.status_code == 201:
            return valid(data["message"]),0
        elif response.status_code == 400:
            return erred("Board or Project is not set. Use switch to set."),1
    

    @login_required
    def delete_project(self,name):
        suffix = SUFFIXES["delete-project"]
        data = {
            "name":name,
        }
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data =  json.loads(response.text)
        if response.status_code == 200:
            return valid(data["message"]),0
        elif response.status_code == 404:
            return erred(data["error"]),1
    
    @login_required
    def delete_board(self,name):
        suffix = SUFFIXES["delete-board"]
        data = {
            "name" : name,
        }
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data =  json.loads(response.text)
        if response.status_code == 200:
            return valid(data["message"]),0
        elif response.status_code == 404:
            return erred(data["error"]),1

    @login_required
    def delete_task(self,alias):
        suffix = SUFFIXES["delete-task"]
        data = {
            "alias" : alias
        }
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data =  json.loads(response.text)
        if response.status_code == 200:
            return valid(data["message"]),0
        elif response.status_code == 404:
            return erred(data["error"]),1

    @login_required
    def show_project(self,name=None):
        suffix = SUFFIXES["show-project"]
        data = {
            "name" : name
        }
        data = json.dumps(data) if name else None
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return data["project"],0
        elif response.status_code == 404:
            return erred(data["error"]),1
        
    @login_required
    def show_board(self):
        suffix = SUFFIXES["show-board"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return data["board"],0
        elif response.status_code == 404:
            return erred(data["error"]),1

    @login_required
    def show_task(self,alias):
        suffix = SUFFIXES["show-task"]
        data = {
            "alias" : alias
        }
        data = json.dumps(data)
        response = requests.get(BASE_URL+suffix,data=data,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return data["task"],0
        elif response.status_code == 404:
            return erred(data["error"]),1
        
    @login_required
    def show_assigned_task(self):
        suffix = SUFFIXES["show-assigned-tasks"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return data["tasks"],0
        elif response.status_code == 404:
            return erred(data["error"]),1
        
    @login_required 
    def set_status(self,alias):
        suffix = SUFFIXES["set-status"]
        
        data = {
            "alias" : alias
        }
        data = json.dumps(data)
        response = requests.post(BASE_URL+suffix,data=data,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return valid(data["message"]),0
        elif response.status_code == 404:
            return erred(data["error"]),1
        
    @login_required
    def status(self):
        suffix = SUFFIXES["current"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return data["current"],0

