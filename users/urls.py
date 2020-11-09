from . import views
from django.urls import path

urlpatterns = [
    path("", views.index),
    path("new", views.new_user),
    path("create", views.register_user),
    path("sign-in", views.sign_in),
    path("get-user", views.get_user),
    path("<uuid:user_id>", views.me),
    path("logout", views.logout)
]
