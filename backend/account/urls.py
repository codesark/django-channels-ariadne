from django.urls import path

from .views import (DashboardView, EmailSignUpView, MobileSignUpView,
                    SignInView, SignUpView, SignOutView)

app_name = "account"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('signout/', SignOutView.as_view(), name="signout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('signup-email/', EmailSignUpView.as_view(), name="signup-email"),
    path('signup-mobile/', MobileSignUpView.as_view(), name="signup-mobile"),
]
