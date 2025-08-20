from django.contrib import admin
from books.models import Book,bookCategory,issueBook
# Register your models here.
@admin.register(Book)
class bookAdmin(admin.ModelAdmin):
    # list_display = ['id','name','catagory','discription']
    list_display = ("name","auther", "addr",)
    exclude = ['slug']

admin.site.register(bookCategory)
# admin.site.register(Book,bookAdmin)
admin.site.register(issueBook)