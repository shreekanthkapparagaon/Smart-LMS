from django.contrib import admin
from books.models import Book,bookCategory,issueBook
from books.forms import BookModelForm
from django.contrib import messages
from import_export.admin import ExportMixin
from import_export import resources
from django.utils.html import format_html


class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('name', 'auther', 'slug', 'catagory__name', 'addr__Address')
        export_order = ('name', 'auther', 'catagory__name', 'addr__Address', 'slug')


@admin.register(Book)
class bookAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = BookResource
    form = BookModelForm

    # Display settings
    list_display = ("name", "auther", "addr")
    list_display_links = ("name",)
    list_per_page = 10
    search_fields = ("name","id")
    ordering = ("name",)
    autocomplete_fields = ["addr"]
    list_select_related = ("catagory", "addr")

    # Form layout (use fieldsets only)
    readonly_fields = ("id", "send_to_device_button")
    exclude = ["slug"]

    fieldsets = (
         ("Book Details", {
        "fields": (  # 👈 First row: ID + Button
            ("name",),                        # 👈 Each field in its own row
            ("auther",),
            ("catagory",),
            ("addr",),
            ("discription",),
        )
    }),
    ("Uploader", {
        "fields": ("id", "send_to_device_button",)
    }),
    )

    # Custom button to send book ID
    def send_to_device_button(self, obj):
        return format_html(
            '<button type="button" class="btn btn-success send-book-id mt-2 mb-2" data-book-id="{}">📡 Send to ESP8266</button>',
            obj.id
        )
    send_to_device_button.short_description = "Write"


    # Export hook
    def get_export_queryset(self, request):
        return self.get_queryset(request)

    # Inject custom template for serial JS
    change_form_template = "admin/books/book/change_form.html"
admin.site.register(bookCategory)
# admin.site.register(Book,bookAdmin)
admin.site.register(issueBook)