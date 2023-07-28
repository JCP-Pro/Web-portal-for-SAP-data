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