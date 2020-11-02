from . import views
from django.urls import path

app_name = "results"

urlpatterns = [
    path("", views.index, name="index")
]
