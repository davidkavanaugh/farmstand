from . import views
from django.urls import path

app_name = "sign_in"

urlpatterns = [
    path("", views.index, name="index")
]
