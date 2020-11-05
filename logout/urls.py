from . import views
from django.urls import path

app_name = "logout"

urlpatterns = [
    path("", views.index, name="index")
]
