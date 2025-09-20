from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Profile


class CustomUserAdmin(UserAdmin):
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

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')

# custome site example
# class MyAdminSite(admin.AdminSite):
#     site_header = "Monty Python administration"
#
# admin_site = MyAdminSite(name="myadmin")
# # admin_site.register()