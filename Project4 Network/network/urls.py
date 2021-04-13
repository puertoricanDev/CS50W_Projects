
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    

    # API Routes

    path("newpost", views.New_Post, name="newpost"),
    path("profile/<str:profuser>", views.profile, name="profile"),
    path("ilike", views.Ilike, name="Ilike"),
    path("ifollow/<int:uid>", views.Ifollow, name="Ifollow"),
    path("<str:fllw>", views.load_post, name="load_p"),
    path("saveedit/<int:pid>", views.saveedit, name="saveedit")
]
