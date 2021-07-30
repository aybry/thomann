from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="lookup_hub/login.html",),
        name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("dictionary/sandbox", views.SandboxView.as_view(), name="sandbox"),
    path("dictionary/<str:slug>", views.DictionaryView.as_view(), name="dictionary"),
    path("backup/", views.GetBackupView.as_view(), name="get_backup"),
    path("guide/", views.GuideView.as_view(), name="guide"),
]
