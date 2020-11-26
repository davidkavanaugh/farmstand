from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # CREATE
    path("", views.UserListView.as_view()),
    # READ, UPDATE
    path('<uuid:user_id>', views.UserDetailView.as_view()),
    # SHOW SIGN-UP FORM
    path("new", views.new),
    # SHOW EDIT FORM
    path("<uuid:user_id>/edit", views.edit),
    # SHOW SIGN-IN FORM
    path("sign-in", views.sign_in),
    # SIGN-OUT
    path("<uuid:user_id>/sign-out", views.sign_out),
    # AUTHENTICATE
    path("authenticate", views.authenticate)
]