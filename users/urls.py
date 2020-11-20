from . import views
from django.urls import path

urlpatterns = [
    path("", views.index),
    path("new", views.new_user),
    path("create", views.register_user),
    path("refresh/<str:stripeId>", views.refresh_stripe),
    path("sign-in", views.sign_in),
    path("get-user", views.get_user),
    path("<uuid:user_id>", views.me),
    path("<uuid:user_id>/edit", views.edit_user),
    path("<uuid:user_id>/edit/cancel", views.cancel_edit_user),
    path("<uuid:user_id>/update", views.update_user),
    path("cart", views.get_cart),
    path("logout", views.logout)
]
