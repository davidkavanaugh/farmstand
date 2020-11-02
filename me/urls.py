from . import views
from django.urls import path

app_name = "me"

urlpatterns = [
    path("", views.index, name="index")
]
