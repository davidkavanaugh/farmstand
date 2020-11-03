from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from . import exceptions
import json
import environ
import requests

env = environ.Env()


def index(request):
    return render(request, "sign-up.html")


def register(request):
    # CHECK IF PASSWORDS MATCH
    try:
        request.session['signUpData'] = request.POST
        if request.POST.get('password1') != request.POST.get('password2'):
            raise exceptions.PasswordMatch(
                'password_match', 'Passwords must match')
        else:
            if "error" in request.session:
                del request.session['error']
            return auth0SignUp(request)
    except exceptions.PasswordMatch:
        request.session["error"] = "Passwords must match."
        return redirect("/sign-up")
    except exceptions.PasswordFormat:
        request.session["error"] = "Password is too weak"
        return redirect("/sign-up")
    except exceptions.UserExists:
        request.session["error"] = "User already exists"
        return redirect("/sign-up")
    except Exception as e:
        print(e)
        request.session["error"] = "Internal server error"
        return redirect("/sign-up")


def auth0SignUp(request):
    user_obj = {
        'client_id': env("AUTH0_CLIENT_ID"),
        'email': request.POST['email'],
        'password': request.POST.get['password1'],
        'connection': env("AUTH0_CONNECTION")
    }
    auth0_user = requests.post(
        env("AUTH0_SIGNUP_DOMAIN"), data=user_obj)
    res = auth0_user.json()
    if "code" in res:
        if res["code"] == "invalid_password":
            raise exceptions.PasswordFormat(
                res["code"], res["message"])
        elif res["code"] == "invalid_signup":
            raise exceptions.UserExists(
                res["code"], "User already exists")
        else:
            raise Exception
    else:  # make user, delete session when done
        return createUserDocument(request)


def createUserDocument(request):
    del request.session["signUpData"]
    pass
