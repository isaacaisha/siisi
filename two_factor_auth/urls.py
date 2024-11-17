from django.urls import path
from .views import (
    registerPage, loginPage, logoutUser,
    password_reset_request, password_reset_done,
    password_reset_confirm, password_reset_complete,
)


urlpatterns = [
    # 2FA Authentications URLs
    path('login', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    
    # Password Reset URLs
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete, name='password_reset_complete'),
]
