from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import User, Address
import json
import requests
import bcrypt
import uuid


def index(request):
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        user_id = request.session["user_id"]
        return redirect("/users/"+user_id)


def new_user(request):
    return render(request, "sign-up.html")


def register_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        request.session['signUpData'] = request.POST
        return redirect('/users/new')
        # if "signUpData" in request.session:
        #     del request.session["signUpData"]
    else:
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
            _id=uuid.uuid1(),
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            farm_name=request.POST["farm_name"],
            email=request.POST["email"],
            address=user_address,
            password=pw_hash,
        )
        new_user.save()
        if "signUpData" in request.session:
            del request.session["signUpData"]
        messages.success(request, "Success! Please Sign in.")
        return redirect('/users/sign-in')


def sign_in(request):
    if "user_id" not in request.session:
        return render(request, "sign-in.html")
    else:
        user_id = request.session["user_id"]
        return redirect("/users/"+user_id)


def get_user(request):
    # get user by email from db
    user = User.objects.filter(email=request.POST["email"])
    if user:
        logged_user = user[0]
        # check if password input matches
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user._id
            return redirect('/users/' + logged_user._id)
        else:
            messages.error(request, "Email / Password incorrect")
    else:
        messages.error(request, "User not found")
    return redirect('/users/sign-in')


def me(request, user_id):
    context = {
        "user": User.objects.get(_id=user_id)
    }
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        return render(request, "me.html", context)


def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('/users/sign-in')
