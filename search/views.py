from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from django.contrib import messages
import json
from users.models import User, Address
import os


def index(request):
    return render(request, "index.html")


def get_farms(request):
    context = {
        "farms": []
    }
    headers = {"apikey": os.getenv("ZIP_KEY")}

    params = (
        ("code", request.POST["zipCode"]),
        ("radius", request.POST["search-radius"]),
        ("country", "us"),
        ("unit", "miles")
    )

    response = requests.get(
        os.getenv("ZIP_DOMAIN"), headers=headers, params=params)
    res = json.loads(response.text)["results"]
    if len(res) == 0:
        messages.error(request, "No Farms Found")
        return redirect("/")
    for location in res:
        addresses = Address.objects.filter(zip_code=location["code"])
        for address in addresses:
            print(address)
            context["farms"].append(User.objects.get(_id=address.user._id))
    return render(request, "search-results.html", context)
