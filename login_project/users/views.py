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

def sign_in(request):
    if request.method == 'GET':

        print("GET METHOD ACCESSED!")
        print("  ")
        form = LoginForm(request.GET)


        if form['user_wf'].value() == None:

            print(f"No User input value: {form['user_wf'].value()}")
            return render(request,'users/login.html', {'form': form})
        
        else: #users/login.html?user_wf=<input value>
            s = requests.Session()
           
            username_wf = form['user_wf'].value() #This gets the value of the input of user_wf
            print(f"user_wf: {username_wf}")
            endpoint_url = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_tasks?user_wf='+username_wf

            #currently user-agent is this python script
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }

            username = Credentials().user #eone
            password = Credentials().password #thebest

            s.auth = HTTPBasicAuth(username, password)

            r_endpoint_session_post = s.post(endpoint_url, auth= s.auth, headers=headers)

            r_endpoint_session_get = s.get(endpoint_url)


            # print(f"this is the POST SESSION: {r_endpoint_session_post.text}")
            # print(" ")
            # print(f"Webservice : {r_endpoint_session_get.text}")
            # print(" ")
            # print(f"Webservice header: {r_endpoint_session_get.headers}")
            print(" ")
            # print(f"Webservice STATUS CODE: {r_endpoint_session_get.status_code}")
            # print(" ")
            # print(f"Webservice request header(what we send to the server): {r_endpoint_session_get.request.headers}")
            # print(" ")

            # print("End")

        
            # check_user(form['user_wf'].value())# check if user exists or not.

            request.session['user_wf'] = username_wf #to pass session name to the next view

            request.session['task_data'] = r_endpoint_session_get.text #Get tasks

            request.session['status_code'] = r_endpoint_session_get.status_code #for handling exceptions such as 404, 500 etc...

            redirect_url = 'tasks'

            return redirect(redirect_url)
    
    else: 
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    


def tasks(request):
    user_session = request.session['user_wf']
    print("HOME ACCESSED")
    print(" ")
    print(f"Printing the user_wf: {user_session}")

    tasks = request.session['task_data']

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
        with open(complete_file_path, 'w') as f:
            f.write(tasks)



    return render(request, 'users/tasks.html',
                   {'user_wf' : user_session,
                    'msg': msg,
                    'task_file_name': task_file_name,
                    'tasks': tasks
                    })

#TODO: Send ID_Proc and Task from table in the api call. Where? to -> http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close
