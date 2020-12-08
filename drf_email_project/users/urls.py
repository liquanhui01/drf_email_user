from django.urls import path
from .views import (
    user_register_view,
    email_verify_view,
    login_verify_view,
    reset_password_view,
    user_list_view,
    user_single_view
)

urlpatterns = [
    path('registration/', user_register_view, name="register"),
    path('email-verify/', email_verify_view, name='email_verify'),
    path('login/', login_verify_view, name="login"),
    path('reset/', reset_password_view, name="reset_password"),
    path('users/', user_list_view, name="users_list"),
    path('user/<str:id>/', user_single_view, name="user_single")
]
