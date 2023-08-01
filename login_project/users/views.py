from django.shortcuts import render, redirect
from .forms import LoginForm, TaskForm, AttachForm
from .config import authenticate_user_wf, request_task
import json

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
    


def tasks_view(request): #For task.html
    username_wf = request.session['user_wf']
    print("VIEWS.PY HOME ACCESSED")
    print(" ")
    print(f"VIEWS.PY Printing the user_wf: {username_wf}")
    attach_data = ''
    msg= ''
    get_tasks = ''
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
    attach_form = AttachForm()

    task_op_wbs_post = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_close?user_wf='+username_wf
    attach_wbs_post = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_attach?user_wf='+username_wf
    pdf_wbs_post = 'http://turing.domain.eonegroup.it:8001/sap/bc/zwf_ext_dsp_bds?user_wf='+username_wf

    if request.method == "POST": #TO CONFIRM OR DECLINE
        print("VIEWS.PY TASK POST METHOD ACCESSED")
        print(" ")
        data = json.loads(json.dumps(dict(request.POST)))
        print(f"VIEWS.PY, this is data: {data}")
        print("")
        # print(f"VIEWS.PY CHECKING DICT-KEY VALUE I NEED FOR CONFIRM OR DECLINE: {data['decline']}")
        #check if key exsist to determine wbs call
        def checkKey(dic, key):
            if key in dic.keys():
                print("VIEWS.PY CHECKING KEY, true")
                print("VIEWS.PY CHECKING KEY, value= ", dic[key])
                return True
            else: 
                print("VIEWS.PY CHECKING KEY, false")
                return False
                
        
        if checkKey(data, 'confirm') == True or checkKey(data, 'decline') == True:
            print("VIEWS.PY conf_dec_form TRUE")
            authenticate_user_wf(request, task_op_wbs_post, data)
            post_status_code = request.session['post_status_code']
            print("")
            print(f"VIEWS.PY STATUS CODE OF THE POST {post_status_code}")
            print(" ")
            if post_status_code == 200: #i will receieve data only if 200 else i will have an error because i don't have any data to manage. When there is an error the response is "There are one or more missing parameters" Therefore
                post_data = eval(request.session['post_data'].strip())
                return_flag = int(post_data['RETURN'])
            if post_status_code == 200 and return_flag == 1:
                print("VIEWS.PY RETURN 1 TRUE")
                get_tasks = request_task(request, username_wf)
            elif post_status_code != 200:
                msg = f"There are one or more missing parameters. Status Error: {[post_status_code]}"
            else:
                msg = f"SAP Error, something went wrong with processing your request." # = RETURN : 0 
                
        elif checkKey(data, 'Loio_id'):
            print("")
            print("VIEWS.PY FETCHING PDF")
            authenticate_user_wf(request, attach_wbs_post, data)
            post_status_code = request.session['post_status_code']
            print("")
            print(f"VIEWS.PY STATUS CODE OF THE POST {post_status_code}")
            print(" ")
            if post_status_code == 200:
                pass # TODO: Send via hidden input also the data for the attach table
            else: f"Status Error: {post_status_code}"

        else: 
            print("VIEWS.PY attachment_call TRUE")
            authenticate_user_wf(request, attach_wbs_post, data)
            post_status_code = request.session['post_status_code']
            print("")
            print(f"VIEWS.PY STATUS CODE OF THE POST {post_status_code}")
            if post_status_code == 200:
                post_data = eval(request.session['post_data'].strip())
                print(f"VIEWS.PY post_data ATTACHMENT: {post_data}")
                print("VIEWS.PY ATTACHMENT PASSED.")
                get_tasks = request_task(request, username_wf)
                print("")
                print(f"VIEWS.PY, This is the request of task content after requesting for attachments: {get_tasks}")
                attach_data = request.session['post_data']
            else: msg = f"Error {post_status_code}"      
    else: print("VIEWS.PY ERROR METHOD")

    return render(request, 'users/tasks.html',
                   {'user_wf' : username_wf,
                    'msg': msg, #error messages
                    'tasks': get_tasks,#task table
                    'conf_dec_form': conf_dec_form,
                    'attach_form' : attach_form,
                    'attachments': attach_data, #attachment table
                    })