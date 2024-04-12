import requests
import json
from rich.text import Text
from rich.console import Console
from kanban.tools import Response,Formats

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


console = Console()

def isOffline(func):
    def wrapper(self,*args,**kwargs):
        try:
            return func(self,*args,**kwargs)
        except requests.ConnectionError:
            return Response("Server is offline.",fmt=Formats.ERRED)
    return wrapper

def login_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.IS_LOGGED_IN:
            return Response('Login to use this.',fmt=Formats.ERRED)
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
    
    @isOffline
    def login(self,username,password):
        suffix = SUFFIXES["login"]
        data = {"username" : username,"password":password}
        response = requests.post(BASE_URL+suffix, data=json.dumps(data))

        self.session = response.cookies.get('sessionid')
        write({"cookie":self.session})
        if response.status_code == 200:
            self.IS_LOGGED_IN = True
            return Response('Logged in succesfully.',fmt=Formats.VALID)
            
        elif response.status_code == 400:
            return Response('Invalid username or password.',fmt=Formats.ERRED)
    
    @isOffline
    @login_required  
    def logout(self):
        suffix = SUFFIXES["logout"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())

        if response.status_code == 200:
            clear()
            return Response('Logged out succesfully.',fmt=Formats.VALID)


    @isOffline   
    def user_registration(self,username,email,password):
        suffix = SUFFIXES["register"]
        data = {
            "username":username,
            "email":email,
            "password":password
        }
        response = requests.post(BASE_URL+suffix,data=json.dumps(data))

        if response.status_code == 200:
            return Response('User created successfully.',fmt=Formats.VALID)
    
    @isOffline
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 400:
            return Response(data["error"],fmt=Formats.ERRED)
    
    @isOffline
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 400:
            return Response(data["error"],fmt=Formats.ERRED)
    
    @isOffline
    @login_required
    def create_board(self,*,name):
        suffix = SUFFIXES["create-board"]
        data = {
            "name":name
        }
        response = requests.post(BASE_URL+suffix,data=json.dumps(data),headers=self.headers())
        data =  json.loads(response.text)
        if response.status_code == 201:
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 400:
            return Response("Project not set. Use switch to set Project.",fmt=Formats.ERRED)
    
    @isOffline
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 400:
            return Response("Board or Project is not set. Use switch to set.",fmt=Formats.ERRED)
    
    @isOffline
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 404:
            return Response(data["error"],fmt=Formats.ERRED)
    
    @isOffline
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 404:
            return Response(data["error"],fmt="error")

    @isOffline
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 404:
            return Response(data["error"],fmt="error")

    @isOffline
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
            return Response(data["project"],fmt=Formats.PROJECT)
        elif response.status_code == 404:
            return Response(data["error"],fmt=Formats.ERRED)

    @isOffline   
    @login_required
    def show_board(self):
        suffix = SUFFIXES["show-board"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return Response(data["board"],fmt=Formats.BOARD)
        elif response.status_code == 404:
            return Response(data["error"],fmt=Formats.ERRED)

    @isOffline
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
            return Response(data["task"],fmt=Formats.TASK)
        elif response.status_code == 404:
            return Response(data["error"],fmt=Formats.ERRED)

    @isOffline    
    @login_required
    def show_assigned_task(self):
        suffix = SUFFIXES["show-assigned-tasks"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return Response(data["tasks"],fmt=Formats.TASKS)
        elif response.status_code == 404:
            return Response(data["error"],fmt=Formats.ERRED)

    @isOffline   
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
            return Response(data["message"],fmt=Formats.VALID)
        elif response.status_code == 404:
            return Response(data["error"],fmt=Formats.ERRED)

    @isOffline   
    @login_required
    def status(self):
        suffix = SUFFIXES["current"]
        response = requests.get(BASE_URL+suffix,headers=self.headers())
        data = json.loads(response.text)
        if response.status_code == 200:
            return Response(data["current"],fmt=Formats.CWS)

