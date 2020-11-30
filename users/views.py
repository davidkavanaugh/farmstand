from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import User, Address
from django.views import View
import json
import requests
import bcrypt
import uuid
import cgi
from random import randint
import users.repository as UsersRepository

class UserListView(View):
    def post(self, request):
        print('creating new user')
        print('checking for errors')
        errors = User.objects.signup_validator(request.POST, request.FILES)
        if len(errors) > 0:
            print('errors')
            for error_type, error_message in errors.items():
                print(error_message)
                messages.error(request, error_message, extra_tags=error_type)
            # redirect the user back to the form to fix the errors
            # save form data in memory before redirecting
            print('redirecting user to correct errors')
            request.session['signUpData'] = request.POST
            return redirect('/users/new')
        else:
            print('no errors. creating stripe account')
            stripe_user = UsersRepository.CreateStripeUser(request.POST['email'], request.POST['first_name'], request.POST['last_name'], request.POST['street_2'], request.POST['city'], request.POST['state'], request.POST['zip_code'])

            print('creating stripe link')
            stripe_link = UsersRepository.CreateStripeLink(stripe_user.id)

            print('saving user address to db')
            user_address = Address(
                street_1=request.POST["street_1"],
                street_2=request.POST["street_2"],
                city=request.POST["city"],
                state=request.POST["state"],
                zip_code=request.POST["zip_code"]
            )
            user_address.save()

            print('hashing pw')
            pw_hash = bcrypt.hashpw(
                request.POST['password_1'].encode(), bcrypt.gensalt()).decode()

            print('creating new user document')
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
            print('user document created in db')

            if 'image' in request.FILES:
                print('saving profile image to user')
                new_user.image=request.FILES['image']
            new_user.save()
            print('deleting form registration data from memory')
            if "signUpData" in request.session:
                del request.session["signUpData"]
            
            print('saving user_id to session')
            user = User.objects.get(_id=new_user._id)
            request.session['user_id'] = user._id

            print('success!')
            messages.success(request, "Success! Please Sign in.")
            return redirect(stripe_link.url)             

class UserDetailView(View):
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.put(*args, **kwargs)
        return super(UserDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, user_id):
        if "user_id" not in request.session:
            return redirect('/users/sign-in')
        else:
            context = {}
            user = User.objects.get(_id=user_id)
            user.id = user._id
            context['user'] = user
            return render(request, "users.self.html", context)

    def patch(self, request, user_id):
        validation_errors = UsersRepository.ValidatePatchRequest(request, request.session['user_id'])
        if validation_errors:
            print('errors')
            return redirect(f"/users/{user_id}/edit")
        else:
            user = User.objects.get(_id=user_id)
            if len(request.POST['password_1']) > 0:
                pw_hash = bcrypt.hashpw(
                    request.POST['password_1'].encode(), bcrypt.gensalt()).decode()
                user.password = pw_hash
            user.first_name=request.POST['first_name']
            user.last_name=request.POST['last_name']
            user.farm_name=request.POST['farm_name']
            user.farm_description=request.POST['farm_description']
            user.email=request.POST['email']
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
            return redirect(f"/users/{user_id}")

def new(request):
    return render(request, "users.new.html")
    
def edit(request, user_id):
    if "user_id" not in request.session:
        return redirect('/users/sign-in')
    else:
        context = {}
        user = User.objects.get(_id=user_id)
        user.id = user._id
        context['user'] = user
        return render(request, "users.edit.html", context)

def sign_in(request):
    if "user_id" not in request.session:
        return render(request, 'users.sign-in.html')
    else:
        user_id = request.session["user_id"]
        return redirect("/users/"+user_id)

def sign_out(request, user_id):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('/users/sign-in')

def authenticate(request):
    # get user by email from db
    user = UsersRepository.FindUserByEmail(request.POST['email'])
    if user:
        # check if password input matches
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user._id
            return redirect('/users/' + user._id)
        else:
            messages.error(request, "Email / Password incorrect")
    else:
        messages.error(request, "User not found")
    return redirect('/users/sign-in')