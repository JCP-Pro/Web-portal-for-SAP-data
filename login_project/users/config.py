from .models import Username

class Credentials:
    user = 'eone'
    password = 'thebest'

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