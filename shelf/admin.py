from django.contrib import admin
from shelf.models import Shelf
# Register your models here.
from import_export.admin import ExportMixin
from import_export import resources
from django.contrib import messages
class ShelfResource(resources.ModelResource):
    class Meta:
        model = Shelf
        fields = ('Address', 'Quantity')
def delete_all_shelfs(modeladmin, request, queryset):
    total = Shelf.objects.count()
    Shelf.objects.all().delete()
    modeladmin.message_user(request, f"🗑️ Deleted all {total} shelfs from the database.", level=messages.WARNING)

delete_all_shelfs.short_description = "🗑️ Delete ALL Shelfs (careful!)"

@admin.register(Shelf)
class shelfAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = ShelfResource
    list_display = ("Address", "Quantity",)
    actions = None
    list_filter = ["Quantity"]
    search_fields = ['Address']
    actions = [delete_all_shelfs]

    list_per_page = 10