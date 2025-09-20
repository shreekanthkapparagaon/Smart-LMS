from django.contrib import admin
from shelf.models import Shelf
# Register your models here.
@admin.register(Shelf)
class shelfAdmin(admin.ModelAdmin):
    list_display = ("Address", "Quantity",)
    actions = None
    list_filter = ["Quantity"]
    search_fields = ['Address']