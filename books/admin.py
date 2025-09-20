from django.contrib import admin
from books.models import Book,bookCategory,issueBook
from books.forms import BookModelForm
from django.contrib import messages
from import_export.admin import ExportMixin
from import_export import resources

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('name', 'auther', 'slug', 'catagory__name', 'addr__Address')
        export_order = ('name', 'auther', 'catagory__name', 'addr__Address', 'slug')





class bookAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = BookResource
    form = BookModelForm
    list_display = ("name","auther", "addr")
    fields = ['id','name','auther','catagory','addr','discription']
    readonly_fields = ('id',)
    exclude = ['slug']
    actions = ['delete_all_books']
    list_per_page = 10
    list_select_related = ('catagory', 'addr')
    search_fields = ('name',)
    ordering = ('name',)
    autocomplete_fields = ['addr']
    list_display_links = ('name',)
    def delete_all_books(modeladmin, request, queryset):
        if not request.user.is_superuser:
            modeladmin.message_user(request, "❌ Only superusers can perform this action.", level=messages.ERROR)
            return
        total = queryset.count()
        Book.objects.all().delete()
        modeladmin.message_user(request, f"🗑️ Deleted all {total} books from the database.", level=messages.WARNING)

    delete_all_books.short_description = "🗑️ Delete ALL books (careful!)"
    def get_export_queryset(self, request):
        return self.get_queryset(request)





admin.site.register(Book,bookAdmin)


admin.site.register(bookCategory)
# admin.site.register(Book,bookAdmin)
admin.site.register(issueBook)