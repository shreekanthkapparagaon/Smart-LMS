from django.contrib import admin
from .models import Article
# Register your models here.
@admin.register(Article)
class articleAdmin(admin.ModelAdmin):
    list_display = ('title','auther',)
    fieldsets = (
        (None, {"fields": ("title", "discription","auther")}),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superusers see all, others see only their own
        if request.user.is_superuser:
            return qs
        return qs.filter(auther=request.user)

    def has_change_permission(self, request, obj=None):
        if obj:
            obj.auther = request.user
        if obj is None or request.user.is_superuser:
            return True
        return obj.auther == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return True
        return obj.auther == request.user

    def save_model(self, request, obj, form, change):
        if not change or not obj.auther:
            obj.auther = request.user
        super().save_model(request, obj, form, change)
