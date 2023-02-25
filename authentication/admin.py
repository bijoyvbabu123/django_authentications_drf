from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    # model = User
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'date_joined']
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','date_joined')
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)