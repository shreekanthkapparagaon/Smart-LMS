from django.shortcuts import render
from books.models import Book,bookCategory
from .models import Shelf, bookCategory
# Create your views here.

def all_books(request):
    books = Book.objects.all()
    return render(request,'books/all_books.html',{"books":books})
def catagories_books(request):
    if request.method == 'GET':
        cat = request.GET.get('category', '')
        if cat != "":
            print(cat)
            catagoryInst = bookCategory.objects.filter(name=cat).first()
            if catagoryInst is not None:
                print("exist")
                print(catagoryInst)
                books = Book.objects.filter(catagory=catagoryInst)
            else:
                books = Book.objects.all()
        else:
            books = Book.objects.all()
        return render(request,'books/catagories.html',{"books":books})
    return render(request,'books/catagories.html')


def books_by_branch(request, branch_code):
    books = Book.objects.filter(catagory__name=branch_code).select_related('catagory', 'addr')
    context = {
        "branch":branch_code,
        'books': books
    }
    return render(request, 'books/branch_books.html', context)
