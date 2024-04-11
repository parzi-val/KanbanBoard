from django.http import JsonResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Project, Board,Task,TaskStatus
import json
from django.contrib.auth.models import User
from datetime import datetime
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login,logout
import django.db


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@login_required
@csrf_exempt
def logout_view(request):
    logout(request)
    request.session.flush()  # Clear all session data
    return JsonResponse({'message': 'Logged out successfully'}, status=200)


@csrf_exempt
def user_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User registered successfully'}, status=200)
        else:
            return JsonResponse(serializer.form.errors, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@login_required
@csrf_exempt
def switch_project_and_board(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project_name = data.get("project")
        board_name = data.get("board")
        
        longResp = f"project {project_name} and " if project_name else ""
        
        if project_name:
            try:
                project = Project.objects.get(name=project_name,Owner = request.user)
                request.session['current_project'] = project_name  # Assign the project name to session

                if not board_name:
                    return JsonResponse({'message':f'Switched to project {project_name}.'},status=200)

            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found.'}, status=400)
            
        if board_name:
            if 'current_project' not in request.session:
                return JsonResponse({'error': 'Project is required.'}, status=400)
            
            project_name = request.session['current_project'] 
            try:
                board = Board.objects.get(name=board_name, project__name=project_name)
                request.session['current_board'] = board_name
                return JsonResponse({'message': f'Switched to {longResp}board {board_name}.'}, status=200)
            except Board.DoesNotExist:
                return JsonResponse({'error': 'Board not found.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@login_required
@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        start_date = datetime.strptime(data.get("start_date"),"%Y-%m-%d").date()
        end_date = datetime.strptime(data.get("end_date"),"%Y-%m-%d").date()
        name = data.get("name")
        desc = data.get("desc")
        if name and desc:
            owner = request.user
            try:
                project = Project.objects.create(
                    name=name,
                    desc=desc,
                    start_date=start_date,
                    end_date=end_date,
                    Owner=owner
                )
            except django.db.utils.IntegrityError:
                return JsonResponse({'error':'Project name already taken, use a different name.'},status=400)
            return JsonResponse({'message': 'Project created successfully.'}, status=201)

        else:
            return JsonResponse({'error': 'Name and description are required.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@login_required
@csrf_exempt
def create_board(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        current_project = request.session.get('current_project')

        if not current_project:
            return JsonResponse({'error': 'No project has been set. Use the switch request to set the project.'}, status=400)

        if name:
            try:
                project = Project.objects.get(name=current_project)
                board = Board.objects.create(
                    name=name,
                    project=project
                )
                return JsonResponse({'message': 'Board created successfully.'}, status=201)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found.'}, status=400)
        else:
            return JsonResponse({'error': 'Name or description is missing.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@login_required
@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        name = data.get('name')
        desc = data.get('desc')
        try:
            assigned = User.objects.get(username=data.get('assigned'))
            reporter = User.objects.get(username=data.get('reporter'))
        except User.DoesNotExist:
            return JsonResponse({'error':'assignee or reporter user does not exist.'})
        alias = "".join([i for i in name if i != " "]).lower()
        current_board = request.session.get('current_board')
        current_project = request.session.get('current_project')
        
        if not current_board:
            return JsonResponse({'error': 'No board has been set. Use the switch request to set the board.'}, status=400)
        
        elif not current_project:
            return JsonResponse({'error': 'No project has been set. Use the switch request to set the project.'}, status=400)

        if name and desc and assigned:
            board = Board.objects.get(name=current_board,project__name = current_project)
            task = Task.objects.create(
                name=name,
                desc=desc,
                assigned=assigned,
                board=board,
                alias=alias,
                reporter=reporter
            )
            return JsonResponse({'message': 'Task created successfully.'}, status=201)
        else:
            return JsonResponse({'error': 'Name or description is missing.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

@login_required
@csrf_exempt
def show_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
        except json.decoder.JSONDecodeError:
            name = request.session.get('current_project') 
        user = request.user
        try:
            project = Project.objects.get(name=name,Owner=user)
            project_data = {
                "Name": project.name,
                "Description": project.desc,
                "Created On": project.creation_date,
                "Duration": f"{project.start_date} - {project.end_date}" if project.start_date and project.end_date else None,
                "Status": project.status,
            }
            if project.boards.exists():
                project_data["Boards"] = [board.name for board in project.boards.all()]

            return JsonResponse({"project" :project_data},status=200)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found."}, status=404)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@login_required
@csrf_exempt
def show_board(request):
    if request.method == "GET":
        name = request.session.get("current_board")
        project_name = request.session.get("current_project")
        try:
            board = Board.objects.get(name=name,project__name=project_name)
            todo = Task.objects.filter(board=board,status=TaskStatus.TODO)
            inprogress = Task.objects.filter(board=board,status=TaskStatus.IN_PROGRESS)
            done = Task.objects.filter(board=board,status=TaskStatus.DONE)
            data = {
                "board" : board.name,
                "todo" : [taskJSON(i) for i in todo],
                "inprogress" : [taskJSON(i) for i in inprogress],
                "done" : [taskJSON(i) for i in done]
                }
            return JsonResponse({"board":data},status=200)
        except Board.DoesNotExist:
            return JsonResponse({"error":"Board not found."},status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

def taskJSON(task:Task):
    data = {
        "name":task.name,
        "desc":task.desc,
        "alias":task.alias,
        "assigned":task.assigned.username,
        "reporter":task.reporter.username,
        "priority":task.priority
    }
    return data

def briefTaskJSON(task):
    data = {
        "name":task.name,
        "board":task.board.name,
        "project":task.board.project.name
    }
    return data

@login_required
def show_task(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        print(data)
        board = request.session.get('current_board')
        try:
            task = Task.objects.get(alias=data.get('alias'))
            if task.board.name != board:
                return JsonResponse({'error':'Task not found'},status=404)
            return JsonResponse({"task":taskJSON(task)},status=200)
        except Task.DoesNotExist:
            return JsonResponse({'error':'Task not found'},status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@login_required
def show_assigned_tasks(request):
    if request.method == 'GET':
        assigned_tasks = Task.objects.filter(assigned=request.user)
        data ={"tasks" : [briefTaskJSON(i) for i in assigned_tasks]}
        return JsonResponse({"tasks":data},status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@login_required
@csrf_exempt
def setStatusTask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        alias = data.get('alias')
        board = request.session.get('current_board')
        print(board)
        try:
            task = Task.objects.get(alias=alias)
            print(task.board)
            if request.user not in (task.board.project.Owner,task.assigned,task.reporter):
                return JsonResponse({'error':'Project not found.'},status=404)
            if task.board.name != board:
                return JsonResponse({'error':'Task does not belong to this board.'},status=204)
            if task.status == TaskStatus.DONE:
                return JsonResponse({'message':'Task is already completed. Use delete to remove the task.'})
            status = TaskStatus.IN_PROGRESS if task.status == TaskStatus.TODO else TaskStatus.DONE
            task.set_status(status)
            task.save()
            return JsonResponse({'message': f'Updated status of task {task.name} -> {status}'},status=200)
        except Task.DoesNotExist:
            return JsonResponse({'error':'Task not found'},status=204)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@login_required
@csrf_exempt
def delete_project(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        try:
            project = Project.objects.get(name=name)
            if request.user != project.Owner:
                return JsonResponse({'error':'Project not found.'},status=404)
            project.delete()
            return JsonResponse({'message':f'Successfully deleted project {name}'},status=200)
        except Project.DoesNotExist:
            return JsonResponse({'error' :'Project not found.'},status=404)


@login_required
@csrf_exempt
def delete_board(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        project = request.session.get('current_project')
        try:
            board = Board.objects.get(name=name,project__name=project)
            if request.user != board.project.Owner:
                return JsonResponse({'error':'Board not found.'},status=404)
            board.delete()
            return JsonResponse({'message':f'Successfully deleted board {name}'},status=200)
        except Board.DoesNotExist:
            return JsonResponse({'error' :'Board not found.'},status=404)
            

@login_required
@csrf_exempt
def delete_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        alias = data.get('alias')
        board = request.session.get('current_board')
        try:
            task = Task.objects.get(alias=alias)
            print(task)
            if request.user not in (task.board.project.Owner,task.assigned,task.reporter):
                return JsonResponse({'error':'Project not found.'},status=404)
            if task.board.name != board:
                return JsonResponse({'error':'Task does not belong to this board.'},status=204)
            task.delete()
            return JsonResponse({'message':f'Successfully deleted task {alias}'},status=200)
        except Project.DoesNotExist:
            return JsonResponse({'error' :'Project not found.'},status=404)
            
@login_required
@csrf_exempt
def current(request):
    if request.method == "GET":
        try:
            project = request.session.get('current_project')
        except KeyError:
            return JsonResponse({'error' :'No project. Use switch to set project.'},status=404)
        try:
            board = request.session.get('current_board')
        except KeyError:
            return JsonResponse({'error' :'No board has been set. Use switch to set board.'},status=404)
        
        data = {k:v for k,v in [("project",project),("board",board)] if v is not None}
        return JsonResponse({'current':data},status=200)
