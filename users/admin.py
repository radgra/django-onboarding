from django.contrib import admin
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from image_cropping import ImageCroppingMixin
# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')}
        ),
    )
    list_display = ['email', 'username']
    '''Admin View for CustomUser'''
admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(ImageCroppingMixin, admin.ModelAdmin):
    '''Admin View for Profile'''
admin.site.register(Profile,ProfileAdmin)

