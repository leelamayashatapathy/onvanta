from django.urls import path

from .views import (
    AcceptInviteView,
    CurrentUserView,
    LoginView,
    RefreshView,
    SetPasswordFromInviteView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('refresh/', RefreshView.as_view(), name='auth-refresh'),
    path('me/', CurrentUserView.as_view(), name='auth-me'),
    path('accept-invite/', AcceptInviteView.as_view(), name='auth-accept-invite'),
    path('set-password-from-invite/', SetPasswordFromInviteView.as_view(), name='auth-set-password-from-invite'),
]
