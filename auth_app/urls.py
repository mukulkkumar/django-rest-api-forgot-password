from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('send-verification-link/', SendEmailView.as_view(), name='send-verification-link'),
    path('reset-password/<slug:uidb64>/<slug:token>/', UserEmailLinkView.as_view(), name='auth-link-verification'),
    path('change-password/', ResetPasswordView.as_view(), name='change-password'),
]
