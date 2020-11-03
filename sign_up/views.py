from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import environ
import requests

env = environ.Env()


def index(request):
    return render(request, "sign-up.html")


def register(request):

    request.session['signUpData'] = request.POST
    if request.POST['password'] != request.POST['confirmPassword']:
        request.session["error"] = "Passwords must match."
        return redirect("/sign-up")
    else:
        if "error" in request.session:
            del request.session['error']
        return auth0SignUp(request)


def auth0SignUp(request):
    user_obj = {
        'client_id': env("AUTH0_CLIENT_ID"),
        'email': request.POST['email'],
        'password': request.POST['password'],
        'connection': env("AUTH0_CONNECTION")

    }
    auth0_user = requests.post(env("AUTH0_SIGNUP_DOMAIN"), data=user_obj)
    res = auth0_user.json()
    if "code" in res:
        if res["code"] == "invalid_password":
            request.session["error"] = res["message"]
            return redirect("/sign-up")
        elif res["code"] == "invalid_signup":
            request.session["error"] = "User already exists"
            return redirect("/sign-up")
        # Todo -- throw catchall error
    else:  # make user, delete session when done
        del request.session["signUpData"]
        return JsonResponse(res)
