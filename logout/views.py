from django.shortcuts import render, redirect


def index(request):
    del request.session["user_id"]
    return redirect('/sign-in')
