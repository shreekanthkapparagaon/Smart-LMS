from django.contrib import admin
from books.models import Book,bookCategory,issueBook
from books.forms import BookModelForm
# Register your models here.
# @admin.register(Book)
# class bookAdmin(admin.ModelAdmin):
#     # list_display = ['id','name','catagory','discription']
#     list_display = ("name","auther", "addr",)
#     exclude = ['slug']

class bookAdmin(admin.ModelAdmin):
    form = BookModelForm
    list_display = ("name","auther", "addr",)
    fields = ['id','name','auther','department',('catagory_display','check'),'catagory','addr','discription']
    readonly_fields = ('id',)
    exclude = ['slug']


admin.site.register(Book,bookAdmin)


admin.site.register(bookCategory)
# admin.site.register(Book,bookAdmin)
admin.site.register(issueBook)