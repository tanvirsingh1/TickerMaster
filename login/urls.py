from django.contrib import admin
from django.urls import path,include
from login import views
urlpatterns = [
    path('login', views._login_window_, name ="Login Window" ),
    path('register', views._register_window_, name="Register Window")
]
