from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import mixins
from .forms import UserCreationEmailForm, UserCreationPhoneNumberForm


# -- Dashboard ---------
class DashboardView(mixins.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')


# -- SignIn ---------

class SignInView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, 'signin.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        error_message = False

        if user is not None and user.is_active is True:
            login(request, user)
            if 'next' in request.GET.keys():
                return redirect(request.GET['next'])
            return redirect("home")
        else:
            error_message = "Invalid username or password"

            return render(request, 'signin.html', {
                "error_message": error_message,
            })


# -- SignOut ---------
class SignOutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        if 'next' in request.GET.keys():
            return redirect(request.GET['next'])
        return redirect("home")


# -- SignUp ---------
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', {})


class EmailSignUpView(View):

    def get(self, request, *args, **kwargs):
        email_form = UserCreationEmailForm()

        return render(request, 'signup-email.html', {
            "form_title": "SignUp with Email",
            "form": email_form.as_p()
        })

    def post(self, request, *args, **kwargs):
        email_form = UserCreationEmailForm(request.POST)

        if email_form.is_valid():
            email_form.save()
            if 'next' in request.GET.keys():
                return redirect(request.GET['next'])
            return redirect("home")
        else:
            return render(request, 'signup-email.html', {
                "form_title": "SignUp with Email",
                "form": email_form.as_p(),
            })


class MobileSignUpView(View):

    def get(self, request, *args, **kwargs):
        mobile_form = UserCreationPhoneNumberForm()

        return render(request, 'signup-mobile.html', {
            "form_title": "SignUp with Mobile",
            "form": mobile_form.as_p()
        })

    def post(self, request, *args, **kwargs):
        mobile_form = UserCreationPhoneNumberForm(request.POST)

        if mobile_form.is_valid():
            mobile_form.save()
            if 'next' in request.GET.keys():
                return redirect(request.GET['next'])
            return redirect("home")
        else:
            return render(request, 'signup-mobile.html', {
                "form_title": "SignUp with Mobile",
                "form": mobile_form.as_p()
            })
