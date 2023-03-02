from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    # model = User
    list_display = ['email', 'auth_provider', 'first_name', 'last_name', 'is_verified', 'is_active', 'date_joined', 'is_staff', 'is_superuser']
    list_filter = ('is_verified', 'is_staff', 'is_active', 'is_superuser', 'auth_provider')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'auth_provider')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'auth_provider', 'first_name', 'last_name', 'is_active','is_staff', 'is_superuser', 'password1', 'password2', 'is_verified'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','date_joined')
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)