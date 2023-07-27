from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import requests
from requests.auth import HTTPBasicAuth
from requests import Session
from .config import Credentials
import json
import os.path

s = requests.Session()

def authenticate_user_wf(request, url, payload):
    username = Credentials().user #eone
    password = Credentials().password #thebest
    payload = payload

    headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

    request_param = request

    s.auth = HTTPBasicAuth(username, password)

    r_endpoint_session_post = s.post(url, auth= s.auth, headers=headers, data= payload)

    r_endpoint_session_get = s.get(url)

    get_session_data(request_param, r_endpoint_session_get)

    #debug
    print("START DEBUG")
    print(" ")
    print(f"this is the POST SESSION: {r_endpoint_session_post.text}")
    print(" ")
    print(f"Webservice : {r_endpoint_session_get.text}")
    print(" ")
    print(f"Webservice header: {r_endpoint_session_get.headers}")
    print(" ")
    print(f"Webservice STATUS CODE: {r_endpoint_session_get.status_code}")
    print(" ")
    print(f"Webservice request header(what we send to the server): {r_endpoint_session_get.request.headers}")
    print(" ")

    print("END DEBUG")

def get_session_data(request, session):
    request.session['data'] = session.text #Get tasks

    request.session['status_code'] = session.status_code #for handling exceptions such as 404, 500 etc...



def sign_in(request):
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
    


def tasks(request):
    user_session = request.session['user_wf']
    session_data_to_get = user_session + '_data'
    print("HOME ACCESSED")
    print(" ")
    print(f"Printing the user_wf: {user_session}")

    tasks = request.session['data']

    status_code = request.session['status_code']

    # print(f"this is the task : {status_code}")

    save_path = "C:/Users/jpineda/Desktop/django_login_form/login_project/static/scripts/users/tasks"

    task_file_name = user_session+'_tasks.json'#example: glini_tasks.json

    complete_file_path = os.path.join(save_path, task_file_name)

    if tasks == "No open task found" and status_code == 200:
        tasks = False
        msg = "No open task found"
    elif status_code == 404:
        tasks = False
        msg = f"Error: {status_code}\n User WF not exist or locked"
    elif status_code == 500:
        tasks = False
        msg = f"Error: {status_code}\n Internal Server Error Occured!"
        # msg = "Internal Server Error Occured!"
    else: 
        msg= ''
        # FIXME: Don't save file of json. Try to store it in a session storage and retrieve it with javascript.
        with open(complete_file_path, 'w') as f:
            f.write(tasks)

    #task operation webservice
    task_op_wbs = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close?user_wf='+user_session

    # authenticate_user_wf(request, task_op_wbs, payload='')#insert the ID_Proc, Task etc.. in payload.

    return render(request, 'users/tasks.html',
                   {'user_wf' : user_session,
                    'msg': msg,
                    'task_file_name': task_file_name,
                    'tasks': tasks
                    })

#TODO: Send ID_Proc and Task from table in the api call. Where? to -> http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close