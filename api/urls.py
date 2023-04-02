from django.urls import path
from . import views

#FOR EVERY NEW VIEW API MUST ADD PATH

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('users/', views.getUsers, name="users"),
    path('users/<str:pk>', views.getUser, name="user")
]