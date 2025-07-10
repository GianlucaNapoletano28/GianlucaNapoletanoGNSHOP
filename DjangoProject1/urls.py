
from django.urls import path
from gianluca_app import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='root_redirect'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('news/', views.news_view, name='news'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('programma-fidelity/', views.programma_fidelity_view, name='programma_fidelity'),
    path('contatti/', views.contatti_view, name='contatti'),
    path('recensioni/', views.recensioni_view, name='recensioni'),
    path('staff/', views.staff_view, name='staff'),
    path('ordini/', views.ordini_view, name='ordini'),
]