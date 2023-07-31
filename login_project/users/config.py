from .models import Username
from requests.auth import HTTPBasicAuth
from requests import Session
import requests
class Credentials:
    user = 'eone'
    password = 'thebest'

#Log on algorithm
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
    if payload == '': #establish if it's a post or get req. Sending a confirm or decline with POST doesn't need a session.get
        r_endpoint_session_get = s.get(url)
        get_session_data(request_param, r_endpoint_session_get, '')
        print("CONFIG.PY START DEBUG")
        print(f"Webservice(GET SESSION) : {r_endpoint_session_get.text}")
        print(" ")
        print(f"Webservice header: {r_endpoint_session_get.headers}")
        print(" ")
        print(f"Webservice STATUS CODE: {r_endpoint_session_get.status_code}")
        print(" ")
        print(f"Webservice request header(what we send to the server): {r_endpoint_session_get.request.headers}")
        print(" ")
        print("CONFIG.PY END DEBUG")
    else:
        get_session_data(request_param, '', r_endpoint_session_post)
        print("CONFIG.PY START DEBUG")
        print(" ")
        print(f"this is the POST SESSION: {r_endpoint_session_post.text}")
        print(" ")
        print(f"Status code of POST SESSION: {r_endpoint_session_post.status_code}")
        print(" ")
        print("CONFIG.PY END DEBUG")

def get_session_data(request, session_get, session_post):
    if session_get != '':
        request.session['get_data'] = session_get.text #Get tasks
        request.session['get_status_code'] = session_get.status_code #for handling exceptions such as 404, 500 etc...
        print(f"CONFIG.PY inside get_session function, GET DATA: Status_code: {session_get.status_code}")
    if session_post!= '':
        request.session['post_data'] = session_post.text
        request.session['post_status_code'] = session_post.status_code
        print(f"CONFIG.PY inside get_session function, POST DATA: Status_code: {session_post.status_code}")


""" def check_user(user):
    model = Username
    if not model.objects.filter(username=user).exists():
        print("New user.")
        return model.objects.create(username=user)
    else : 
        return print("User already exists.") """
    





#test code
""" test_url = 'https://httpbin.org/headers'
r_test_session_post = s.post(test_url, auth=s.auth)
r_test_session_get = s.get(test_url)
r_t_s = s.get('https://httpbin.org/headers?user_wf=something&password_wf=asdasd')

print(f"Test session : {r_test_session_get.text}")
print(" ")
print(f"Test session : {r_test_session_get.status_code}")
print(" ")
print(f"This IS THE WEBSITE WITH THE GET I AM SENDING IN THE FORM: {r_t_s.text}")
print(" ")
print(f"This IS THE WEBSITE STATUS CODE: {r_t_s.status_code}") """