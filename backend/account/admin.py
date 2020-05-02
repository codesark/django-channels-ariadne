from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OldUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeAdminForm, UserCreationAdminForm
from .models import OTP

User = get_user_model()


class UserAdmin(OldUserAdmin):
    form = UserChangeAdminForm
    fieldsets = OldUserAdmin.fieldsets + (
        (_('Details'), {'fields': ('avatar',
                                   'dateOfBirth', 'gender', 'bio', 'phone_number')}),
    )
    readonly_fields = ('date_joined', 'last_login')

    add_form = UserCreationAdminForm

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('first_name', 'last_name',  'email', 'phone_number', 'username', 'password1', 'password2'),
        }
        ),
    )

    list_display = ('username', 'email', 'phone_number',
                    'is_active', 'last_login')


class OTPAdmin(admin.ModelAdmin):
    class Meta:
        model = OTP

    readonly_fields = ('generation_time', 'otp_age', 'is_expired')
    list_display = ('id', 'email', 'phone_number', 'otp_age', 'is_expired')


admin.site.register(User, UserAdmin)
admin.site.register(OTP, OTPAdmin)
