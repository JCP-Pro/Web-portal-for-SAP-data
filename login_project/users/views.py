from django.shortcuts import render, redirect
from .forms import LoginForm, TaskForm, FileForm
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

        print(" VIEWS.PY GET METHOD ACCESSED!")
        print("  ")
        form = LoginForm(request.GET)


        if form['user_wf'].value() == None:

            print(f"VIEWS.PY No User input value: {form['user_wf'].value()}")
            return render(request,'users/login.html', {'form': form})
        
        else: #users/login.html?user_wf=<input value>
           
            username_wf = form['user_wf'].value() #This gets the value of the input of user_wf
            print(f"VIEWS.PY user_wf: {username_wf}")
            endpoint_url = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_tasks?user_wf='+username_wf

            authenticate_user_wf(request, endpoint_url, '')

            request.session['user_wf'] = username_wf #to pass session name to the next view

            redirect_url = 'tasks'

            return redirect(redirect_url)
    
    else: 
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    

def request_task(request, user_s):
    endpoint_url = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_tasks?user_wf='+user_s
    authenticate_user_wf(request, endpoint_url, '') #no payload in a GET
    return request.session['get_data']

def tasks_view(request): #For task.html
    user_session = request.session['user_wf']
    print("VIEWS.PY HOME ACCESSED")
    print(" ")
    print(f"VIEWS.PY Printing the user_wf: {user_session}")
    attach_data = ''
    msg= ''
    if request.method == "GET":
        print("VIEWS.PY Request.method = True")
        get_tasks = request.session['get_data'] # Table data
        get_status_code = request.session['get_status_code']

        if get_tasks == "No open task found" and get_status_code == 200:
            get_tasks = False
            msg = "No open task found"
        elif get_status_code == 404:
            get_tasks = False
            msg = f"Error: {get_status_code}\n User WF not exist or locked"
        elif get_status_code == 500:
            get_tasks = False
            msg = f"Error: {get_status_code}\n Internal Server Error Occured!"
        else: 
            msg= ''
        

    # -------------------------------------------------------------------------------------
    #task operation webservice
    conf_dec_form = TaskForm()
    file_form = FileForm()

    task_op_wbs_post = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close?user_wf='+user_session
    attach_wbs_post = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_attach?user_wf='+user_session

    if request.method == "POST": #TO CONFIRM OR DECLINE
        print("VIEWS.PY TASK POST METHOD ACCESSED")
        print(" ")
        data = json.loads(json.dumps(dict(request.POST)))
        if conf_dec_form['data'].value() != None: #input fields value are flags to determine which wbs to call.
            print("VIEWS.PY conf_dec_form TRUE")
            authenticate_user_wf(request, task_op_wbs_post, data)
        else: 
            print("VIEWS.PY attachment_call TRUE")
            authenticate_user_wf(request, attach_wbs_post, data)

        post_status_code = request.session['post_status_code']
        print("")
        print(f"VIEWS.PY STATUS CODE OF THE POST {post_status_code}")
        if post_status_code == 200 and request.session['post_data'] == '{ "RETURN":" 1",  }':
            if request.session['post_data'] == '{ "RETURN":" 1",  }':
                # endpoint_url = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_tasks?user_wf='+user_session
                # authenticate_user_wf(request, endpoint_url, '')
                get_tasks = request_task(request, user_session)
                # msg= '' #no error messages
                # get_tasks = request.session['get_data']
            else: msg = f"Error, something went wrong with processing your request." # = RETURN : 0 
        elif post_status_code == 200:
            print("VIEWS.PY correct conditional passed.")
            get_tasks = request_task(request, user_session)
            attach_data = request.session['post_data']
        else: msg = f"Error {post_status_code}"
    else: print("VIEWS.PY ERROR METHOD")

    return render(request, 'users/tasks.html',
                   {'user_wf' : user_session,
                    'msg': msg, #error messages
                    'tasks': get_tasks,#task table
                    'conf_dec_form': conf_dec_form,
                    'file_form' : file_form,
                    'attachments': attach_data, #attachment table
                    })