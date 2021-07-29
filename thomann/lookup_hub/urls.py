from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", auth_views.LoginView.as_view(
        template_name="lookup_hub/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("dictionary/sandbox", views.SandboxView.as_view(), name="sandbox"),
    path("dictionary/<str:slug>", views.DictionaryView.as_view(), name="dictionary"),
    path("guide/", views.GuideView.as_view(), name="guide"),
]
