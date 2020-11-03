from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from . import exceptions
from sign_up.models import User, Address
import json
import environ
import requests

env = environ.Env()


def index(request):
    if "error" not in request.session:
        if "signUpData" in request.session:
            del request.session["signUpData"]
    return render(request, "sign-up.html")


def register(request):
    # CHECK IF PASSWORDS MATCH
    try:
        request.session['signUpData'] = request.POST
        if request.POST.get('password_1') != request.POST.get('password_2'):
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
        print("ERROR", e)
        request.session["error"] = "Internal server error"
        return redirect("/sign-up")


def auth0SignUp(request):
    user_obj = {
        'client_id': env("AUTH0_CLIENT_ID"),
        'email': request.POST['email'],
        'password': request.POST['password_1'],
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
    else:
        return create_user(request, res["_id"])


def create_user(request, auth0_id):
    try:
        user_address = Address(
            street_1=request.POST["street_1"],
            street_2=request.POST["street_2"],
            city=request.POST["city"],
            state=request.POST["state"],
            zip_code=request.POST["zip_code"]
        )
        user_address.save()

        new_user = User(
            auth0_id=auth0_id,
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            address=user_address
        )
        new_user.save()
        print("REGISTRATION SUCCESSFUL")
        del request.session["signUpData"]
        return redirect('/sign-up/success')
    except:
        raise Exception


def success(request):
    return render(request, "success.html")
