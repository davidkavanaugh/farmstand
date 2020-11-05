from . import views
from django.urls import path

urlpatterns = [
    path("", views.redir),
    path("<uuid:user_id>", views.index)
]
