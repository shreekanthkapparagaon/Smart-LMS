from core.admin import custom_admin_site

from django.contrib import admin
from shelf.models import Shelf
# Register your models here.
from import_export.admin import ExportMixin
from import_export import resources
class ShelfResource(resources.ModelResource):
    class Meta:
        model = Shelf
        fields = ('addr', 'qunt')



class shelfAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = ShelfResource
    list_display = ("addr", "qunt",)
    actions = None
    list_filter = ["qunt"]
    search_fields = ['addr',"qunt"]

    list_per_page = 10

custom_admin_site.register(Shelf,shelfAdmin)