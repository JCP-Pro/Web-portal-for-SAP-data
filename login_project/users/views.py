from django.shortcuts import render, redirect
from .forms import LoginForm, TaskForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import requests
from requests.auth import HTTPBasicAuth
from requests import Session
from .config import Credentials, authenticate_user_wf
import json
import os.path

s = requests.Session()

def login_view(request): #For login.html
    if request.method == 'GET':

        print("GET METHOD ACCESSED!")
        print("  ")
        form = LoginForm(request.GET)


        if form['user_wf'].value() == None:

            print(f"No User input value: {form['user_wf'].value()}")
            return render(request,'users/login.html', {'form': form})
        
        else: #users/login.html?user_wf=<input value>
           
            username_wf = form['user_wf'].value() #This gets the value of the input of user_wf
            print(f"user_wf: {username_wf}")
            endpoint_url = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_tasks?user_wf='+username_wf

            authenticate_user_wf(request, endpoint_url, '')

            request.session['user_wf'] = username_wf #to pass session name to the next view

            redirect_url = 'tasks'

            return redirect(redirect_url)
    
    else: 
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    


def tasks_view(request): #For task.html
    user_session = request.session['user_wf']
    print("HOME ACCESSED")
    print(" ")
    print(f"Printing the user_wf: {user_session}")

    tasks = request.session['data']

    status_code = request.session['status_code']

    # print(f"this is the task : {status_code}")

    if tasks == "No open task found" and status_code == 200:
        tasks = False
        msg = "No open task found"
    elif status_code == 404:
        tasks = False
        msg = f"Error: {status_code}\n User WF not exist or locked"
    elif status_code == 500:
        tasks = False
        msg = f"Error: {status_code}\n Internal Server Error Occured!"
    else: 
        msg= ''
        
    
    #task operation webservice
    form = TaskForm()
    task_op_wbs_post = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close?user_wf='+user_session

    print(f"PRINTING THE REQUEST {request}")
    if request.method == "GET":
        print("TASK GET METHOD ACCESSED")
        data = json.dumps(dict(request.GET))
        task_op_wbs_get = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close?user_wf='+user_session+data
        
        authenticate_user_wf(request, task_op_wbs_get, '')
        print(f"DATA IN THE GET METHOD: {data}")
    elif request.method == "POST":
        print("TASK POST METHOD ACCESSED")
        data = json.loads(json.dumps(dict(request.POST)))
        authenticate_user_wf(request, task_op_wbs_post, data)
        # redirect_url = 'task'
        # return redirect(redirect_url)
    else: print("ERROR METHOD")

    return render(request, 'users/tasks.html',
                   {'user_wf' : user_session,
                    'msg': msg,
                    'tasks': tasks,
                    'form': form,
                    })

#TODO: Send ID_Proc and Task from table in the api call. Where? to -> http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close