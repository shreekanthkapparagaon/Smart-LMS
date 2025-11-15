from core.admin import custom_admin_site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.html import format_html
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
    readonly_fields = ('id','send_to_device_button',)
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": (("id",'send_to_device_button'),"email", "password")}),
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
    def send_to_device_button(self, obj):
        return format_html(
             '''
                <button type="button" onclick="copyText(this)" 
                        class="btn btn-primary btn-sm rounded-pill px-3 shadow-sm"  
                        data-book-id="{}">
                    📋 Copy ID
                </button>
                <script>
                    function copyText(button) {{
                        const bookId = button.getAttribute("data-book-id");
                        navigator.clipboard.writeText(bookId).then(() => {{
                            // Show a subtle toast instead of alert
                            const toast = document.createElement("div");
                            toast.innerText = "Copied: " + bookId;
                            toast.style.position = "fixed";
                            toast.style.bottom = "20px";
                            toast.style.right = "20px";
                            toast.style.background = "#28a745";
                            toast.style.color = "white";
                            toast.style.padding = "8px 12px";
                            toast.style.borderRadius = "6px";
                            toast.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
                            document.body.appendChild(toast);
                            setTimeout(() => toast.remove(), 2000);
                        }}).catch(err => {{
                            console.error("Failed to copy ID: ", err);
                        }});
                    }}
                </script>
            ''',
            obj.id
        )

    send_to_device_button.short_description = " : "


class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')
    list_per_page = 10


custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(Profile, profileAdmin)