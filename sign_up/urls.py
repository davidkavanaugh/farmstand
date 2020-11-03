from . import views
from django.urls import path

app_name = "sign_up"

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("success", views.success, name="success")
]
