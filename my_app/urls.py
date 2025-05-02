from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

urlpatterns = [
    # path('', views.accueil, name='accueil'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Page d'accueil protégée
    path('', login_required(lambda request: render(request, 'my_app/dashboard.html')), name='home'),
]
