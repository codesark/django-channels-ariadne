import unicodedata

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from .utils import random_string_generator

User = get_user_model()


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class UserChangeAdminForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserCreationAdminForm(BaseUserCreationForm):

    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))

    email = forms.EmailField(label='Email', max_length=254)
    phone_number = PhoneNumberField()

    username = UsernameField(
        label='Username', widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(UserCreationAdminForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['phone_number'].required = False

    error_messages = {
        'invalid_first_name': _("First Name is not valid"),
        'invalid_last_name': _("Last Name is not valid"),
        'invalid_email': _("Email is not valid"),

        'duplicate_email': _("Provided Email already exists."),
        'duplicate_username': _("Provided Username already exists."),
        'duplicate_phone_number': _("Provided Phone Number already exists."),

        'email_or_phone_not_found': _("You must enter an Email or Phone Number"),
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) > 254 or len(first_name) < 3:
            raise forms.ValidationError(
                self.error_messages['invalid_first_name'])
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) > 254 or len(last_name) < 3:
            raise forms.ValidationError(
                self.error_messages['invalid_last_name'])
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if username is not None and len(username) > 0:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['duplicate_username'])
        else:
            # generate a unique username
            fname = str(
                self.cleaned_data['first_name']).lower().replace(' ', '')
            lname = str(self.cleaned_data['last_name']
                        ).lower().replace(' ', '')
            while True:
                username = ''.join([fname, lname, random_string_generator()])
                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    return username
              

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        if email != '' and email != ' ':
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError(self.error_messages['duplicate_email'])
        return email

    def clean_phone_number(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data['phone_number']

        if phone_number != '' and phone_number != ' ':
            try:
                User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return phone_number
            raise forms.ValidationError(
                self.error_messages['duplicate_phone_number'])

        # if email is None and phone_number is None:
        #   if len(email) == 0 and len(phone_number) == 0:
        #     raise forms.ValidationError(self.error_messages['email_or_phone_not_found'])

        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email",
                  "phone_number", "username")

    def clean(self):

        try:
            email = self.cleaned_data['email']
        except KeyError:
            email = ''

        try:
            phone_number = self.cleaned_data['phone_number']
        except KeyError:
            phone_number = ''

        if email == '' and phone_number == '':
            raise forms.ValidationError(
                self.error_messages['email_or_phone_not_found'])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user


class UserCreationEmailForm(UserCreationAdminForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationEmailForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget = forms.HiddenInput()
        self.fields['username'].widget = forms.HiddenInput()

        self.fields.pop('phone_number')
        self.fields.pop('username')


class UserCreationPhoneNumberForm(UserCreationAdminForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationPhoneNumberForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.HiddenInput()
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['username'].label = "Username email or phone number"

        self.fields.pop('email')
        self.fields.pop('username')


class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username, Email or Phone number"

        # required_css_class = 'required'  # pylint: disable=unused-variable


class AdminPasswordChangeForm(PasswordChangeForm):
    required_css_class = 'required'
