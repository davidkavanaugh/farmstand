from django.shortcuts import render, redirect
from django.http import JsonResponse
from sign_up.models import User


def redir(request):
    if "user_id" not in request.session:
        return redirect('/sign-in')
    else:
        user_id = request.session["user_id"]
        return redirect("/me/"+user_id)


def index(request, user_id):
    context = {
        "user": User.objects.get(id=user_id)
    }
    if "user_id" not in request.session:
        return redirect('/sign-in')
    else:
        return render(request, "me.html", context)
