from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from . import exceptions
from .models import User, Address
import json
import environ
import requests
import bcrypt
import uuid

env = environ.Env()


def index(request):
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        user_id = request.session["user_id"]
        return redirect("/users/"+user_id)


def new_user(request):
    if "error" not in request.session:
        if "signUpData" in request.session:
            del request.session["signUpData"]
    return render(request, "sign-up.html")


def register_user(request):
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
        return redirect("/users/new")
    except exceptions.PasswordFormat:
        request.session["error"] = "Password is too weak"
        return redirect("/users/new")
    except exceptions.UserExists:
        request.session["error"] = "User already exists"
        return redirect("/users/new")
    except Exception as e:
        print("ERROR", e)
        request.session["error"] = "Internal server error"
        return redirect("/users/new")


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

        pw_hash = bcrypt.hashpw(
            request.POST['password_1'].encode(), bcrypt.gensalt()).decode()

        new_user = User(
            id=uuid.uuid1(),
            auth0_id=auth0_id,
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            address=user_address,
            password=pw_hash,
        )
        new_user.save()
        print("REGISTRATION SUCCESSFUL")
        del request.session["signUpData"]
        return redirect('/users/new/success')
    except:
        raise Exception


def sign_up_success(request):
    return render(request, "sign-up-success.html")


def sign_in(request):
    if "user_id" not in request.session:
        return render(request, "sign-in.html")
    else:
        user_id = request.session["user_id"]
        return redirect("/users/"+user_id)


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
                return redirect('/users/' + logged_user.id)
            else:
                messages.error(request, "Email / Password incorrect")
        else:
            messages.error(request, "User not found")
        return redirect('/users/sign-in')

    except Exception:
        raise Exception


def me(request, user_id):
    context = {
        "user": User.objects.get(id=user_id)
    }
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        return render(request, "me.html", context)


def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('/users/sign-in')
