from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import environ
import requests


def index(request):
    return render(request, "sign-in.html")


def get_user(request):
    env = environ.Env()
    auth_payload = {
        'grant_type': 'password',
        'client_id': env("AUTH0_CLIENT_ID"),
        'username': request.POST['email'],
        'password': request.POST['password']
    }
    headers = {'content-type': "application/x-www-form-urlencoded"}
    auth0_token = requests.post(
        env("AUTH0_SIGNIN_DOMAIN"), auth_payload, headers)
    res = auth0_token
    print(res)
    return HttpResponse(res)
