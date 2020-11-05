from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from sign_up.models import User
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, "sign-in.html")


def get_user(request):
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

    try:
        # get user by email from db
        user = User.objects.filter(email=request.POST["email"])
        if user:
            logged_user = user[0]
            # check if password input matches
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/me')
            else:
                messages.error(request, "Email / Password incorrect")
        else:
            messages.error(request, "User not found")
        return redirect('/sign-in')

    except Exception:
        raise Exception
