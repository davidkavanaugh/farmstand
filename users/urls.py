from . import views
from products import views as products_views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # CREATE
    path("", views.UserListView.as_view()),
    # READ, UPDATE
    path('<uuid:user_id>', views.UserDetailView.as_view()),
    # SHOW EDIT FORM
    path("<uuid:user_id>/edit", views.edit),
    # SIGN-OUT
    path("<uuid:user_id>/sign-out", views.sign_out),
    # LIST USER PRODUCTS
    path("<uuid:user_id>/products", products_views.ProductListView.as_view()),
    # SHOW SIGN-UP FORM
    path("new", views.new),
    # SHOW SIGN-IN FORM
    path("sign-in", views.sign_in),
    # AUTHENTICATE
    path("authenticate", views.authenticate)
]