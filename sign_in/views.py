from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from sign_up.models import User
import bcrypt


def index(request):
    return render(request, "sign-in.html")


def get_user(request):
    pass
    # env = environ.Env()
    # auth_payload = {
    #     'grant_type': 'password',
    #     'client_id': env("AUTH0_CLIENT_ID"),
    #     'username': request.POST['email'],
    #     'password': request.POST['password']
    # }
    # headers = {'content-type': "application/x-www-form-urlencoded"}
    # auth0_token = requests.post(
    #     env("AUTH0_SIGNIN_DOMAIN"), auth_payload, headers)
    # res = auth0_token
    # print(res)
    # # return HttpResponse(res)

    # try:
    #     # get user by email from db
    #     user = User.objects.get(email=request.POST["email"])
    #     # check if password input matches
    #     password = request.POST["password"].encode('utf8')
    #     hashed = user.password
    #     # Check that an unhashed password matches one that has previously been
    #     if bcrypt.checkpw(password, hashed):
    #         print("It Matches!")
    #     else:
    #         print("It Does not Match :(")
    # except Exception:
    #     raise Exception
