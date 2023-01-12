from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import (EmailVerificationTemplateView, ProfileUpdateView,
                         UserLoginView, UserRegistrationCreateView, logout)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', UserRegistrationCreateView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(ProfileUpdateView.as_view()), name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationTemplateView.as_view(), name='email_verification'),
]
