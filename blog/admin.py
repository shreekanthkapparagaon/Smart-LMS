from django.contrib import admin
from .models import Article
# Register your models here.
@admin.register(Article)
class articleAdmin(admin.ModelAdmin):
    list_display = ('title','slug',)
    fieldsets = (
        (None, {"fields": ("title", "discription")}),
    )