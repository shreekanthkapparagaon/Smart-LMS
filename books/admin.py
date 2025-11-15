from django.contrib import admin
from books.models import Book,bookTag,issueBook
from books.forms import BookAdminForm
from import_export.admin import ExportMixin
from import_export import resources
from django.utils.html import format_html
from django.contrib import messages
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from shelf.models import Shelf
from core.admin import custom_admin_site
from import_export.admin import ImportExportModelAdmin

def mark_as_returned(modeladmin, request, queryset):
    updated = queryset.update(is_returned=True)
    modeladmin.message_user(
        request,
        f"{updated} post(s) marked as Returned.",
        messages.SUCCESS
    )



class BookResource(resources.ModelResource):
    class Meta:
        model = Book


class bookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    form = BookAdminForm


    # Display settings
    list_display = ("name", "auther", "addr")
    list_per_page = 10
    search_fields = ("name","id")
    ordering = ("name",)
    list_select_related = ("addr",)

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
        "fields": (("id", "send_to_device_button",),)
    }),
    )

    # Custom button to send book ID
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


    # Export hook
    def get_export_queryset(self, request):
        return self.get_queryset(request)

    # Inject custom template for serial JS
    add_form_template = "admin/books/book/change_form.html"
    class Media:
        js = ('js/book_recomend.js',) 
        pass



class issueBookAdmin(admin.ModelAdmin):
    change_form_template = "admin/books/issuebook/issuebook_change_form.html"
    list_display = ('book', 'user', 'issued_on', 'is_returned')
    exclude=("is_returned",)
    actions=[mark_as_returned]
    autocomplete_fields = ['user','book']
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/return/', self.admin_site.admin_view(self.process_return), name='issuebook-return'),
        ]
        return custom_urls + urls

    def process_return(self, request, pk):
        issue = get_object_or_404(issueBook, pk=pk)
        issue.is_returned = True

        # Get or create shelf
        addr, created = Shelf.objects.get_or_create(addr="On Table")
        if created:
            self.message_user(request, f"🆕 Shelf created: '{addr.addr}'", level=messages.INFO)

        # Update book location
        book = issue.book
        book.addr = addr
        book.save()

        issue.save()
        self.message_user(request, f"✅ Book '{book.name}' marked as returned and placed on shelf '{addr.addr}'.", level=messages.SUCCESS)
        return redirect(f'/admin/books/issuebook/{pk}/change/')

class tagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_per_page = 10
    search_fields = ("name","id")

custom_admin_site.register(bookTag,tagAdmin)
custom_admin_site.register(Book,bookAdmin)
custom_admin_site.register(issueBook,issueBookAdmin)