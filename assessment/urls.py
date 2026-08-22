from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('aptitude-ready/', views.aptitude_ready, name='aptitude_ready'),
    path('assess-aptitude/', views.assess_aptitude, name='assess_aptitude'),
    path('preference-ready/', views.preference_ready, name='preference_ready'),
    path('assess-preference/', views.assess_preference, name='assess_preference'),
    path('loading/', views.loading, name='loading'),
    path('result/', views.result, name='result'),
]
