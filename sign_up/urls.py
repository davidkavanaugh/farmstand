from . import views
from django.urls import path

app_name = "signup"

urlpatterns = [
    path("", views.index, name="index")
]
