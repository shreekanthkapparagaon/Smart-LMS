from core.admin import custom_admin_site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Profile

from import_export.admin import ExportMixin
from import_export import resources

class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_staff', 'is_active', 'date_joined')
        export_order = ('id', 'email', 'is_staff', 'is_active', 'date_joined')


class CustomUserAdmin(ExportMixin,UserAdmin):
    resource_class = UserResource
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ('id',)
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": (("id"),"email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",'id')
    ordering = ("email",)
    list_per_page = 10



class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')
    list_per_page = 10


custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(Profile, profileAdmin)