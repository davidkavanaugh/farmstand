from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from django.contrib import messages
import json
from users.models import User, Address


def index(request):
    return render(request, "index.html")


def get_farms(request):
    context = {
        "farms": []
    }
    headers = {"apikey": "67f20620-2093-11eb-9f9f-530d52d6fa49"}

    params = (
        ("code", request.POST["zipCode"]),
        ("radius", request.POST["search-radius"]),
        ("country", "us"),
        ("unit", "miles")
    )

    response = requests.get(
        'https://app.zipcodebase.com/api/v1/radius', headers=headers, params=params)
    res = json.loads(response.text)["results"]
    if len(res) == 0:
        messages.error(request, "No Farms Found")
        return redirect("/")
    for location in res:
        addresses = Address.objects.filter(zip_code=location["code"])
        for address in addresses:
            context["farms"].append(User.objects.get(id=address.user.id))
    return render(request, "search-results.html", context)
