from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import User, Address
import os
import json
import requests
import bcrypt
import uuid
import stripe
from random import randint
stripe.api_key = os.getenv("STRIPE_API_KEY")

def index(request):
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        user_id = request.session["user_id"]
        return redirect("/users/"+user_id)


def new_user(request):
    return render(request, "sign-up.html")

def refresh_stripe(request, stripeId):
    user = User.objects.get(stripeId=stripeId)
    stripe_user = stripe.Account.create(
        type='express',
        country="US",
        email=user.email,
        individual={
            "id_number": "000000000",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "address": {
                "line1": "address_full_match​",
                "line2": user.address.street_2,
                "city": user.address.city,
                "state": user.address.state,
                "postal_code": user.address.zip_code
            }
        },
        business_type="individual",
        default_currency="USD"
    )
    stripe_link = stripe.AccountLink.create(
        account=stripe_user.id,
        refresh_url=f"http://localhost:8000/users/refresh/{stripeId}",
        return_url="http://localhost:8000/users/sign-in",
        type="account_onboarding",
    )    
    return redirect(stripe_link.url)

def register_user(request):
    errors = User.objects.signup_validator(request.POST, request.FILES)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        request.session['signUpData'] = request.POST
        return redirect('/users/new')
    else:
        stripe_user = stripe.Account.create(
            type='express',
            country="US",
            email=request.POST['email'],
            individual={
                "id_number": "000000000",
                "first_name": request.POST['first_name'],
                "last_name": request.POST['last_name'],
                "address": {
                    "line1": "address_full_match​",
                    "line2": request.POST['street_2'],
                    "city": request.POST['city'],
                    "state": request.POST['state'],
                    "postal_code": request.POST['zip_code']
                }
            },
            business_type="individual",
            default_currency="USD"
        )
        stripe_link = stripe.AccountLink.create(
            account=stripe_user.id,
            refresh_url=f"http://localhost:8000/users/refresh/{stripe_user.id}",
            return_url="http://localhost:8000/users/sign-in",
            type="account_onboarding",
        )
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
            instructions=request.POST['instructions'],
            password=pw_hash,
            address=user_address,
            stripeId=stripe_user.id
        )
        if 'image' in request.FILES:
            new_user.image=request.FILES['image']
        new_user.save()
        user = User.objects.get(_id=new_user._id)
        if "signUpData" in request.session:
            del request.session["signUpData"]
        request.session['user_id'] = user._id
        messages.success(request, "Success! Please Sign in.")
        return redirect(stripe_link.url)


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
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        context = {}
        user = User.objects.get(_id=user_id)
        user.id = user._id
        context['user'] = user
        return render(request, "me.html", context)

def edit_user(request, user_id):
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        context = {}
        user = User.objects.get(_id=user_id)
        user.id = user._id
        context['user'] = user
        return render(request, "edit.html", context)

def update_user(request, user_id):
    errors = User.objects.update_validator(request.POST, request.FILES, request.session['user_id'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        request.session['postData'] = request.POST
        return redirect(f'/users/{user_id}/edit')
    else: 
        user = User.objects.get(_id=user_id)
        if len(request.POST['password_1']) > 0:
            pw_hash = bcrypt.hashpw(
                request.POST['password_1'].encode(), bcrypt.gensalt()).decode()
            user.password = pw_hash
        user.first_name=request.POST["first_name"]
        user.last_name=request.POST["last_name"]
        user.farm_name=request.POST["farm_name"]
        user.farm_description=request.POST["farm_description"]
        user.email=request.POST["email"]
        user.instructions=request.POST['instructions']
        user.address.street_1=request.POST['street_1']
        user.address.street_2=request.POST['street_2']
        user.address.city=request.POST['city']
        user.address.state=request.POST['state']
        user.address.zip_code=request.POST['zip_code']
        if 'image' in request.FILES:
            user.image=request.FILES['image']
        user.address.save()
        user.save()
        if "postData" in request.session:
            del request.session["postData"]
        messages.success(request, "Profile Updated!", extra_tags="update")

    return redirect(f'/users/{user_id}')

def cancel_edit_user(request, user_id):
    return redirect(f'/users/{user_id}')

def get_order(request, order_id):
    context = {}
    return render(request, "order.html", context)

def all_orders(request):
    context = {}
    return render(request, 'orders.html', context)

def get_cart(request):
    return render(request, "shopping-cart.html")


def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('/users/sign-in')
