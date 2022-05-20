from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='Index'),
    path('Login', views.Login, name='Login'),
    path('signup', views.signup, name='signup'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('Category/<str:genre>/', views.Category, name='Category'),
    path('register_otp', views.register_otp, name='register_otp'),
    path('view/<int:sno>/', views.view, name='view'),
    path('Contact', views.Contact, name='Contact'),
    path('profile', views.profile, name='profile'),
    path('logout_user', views.logout_user, name='logout_user')
    ]
