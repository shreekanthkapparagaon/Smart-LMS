from django.shortcuts import render
# from blog.models import Article
from books.models import bookCategory

# Create your views here.
def home(request):
    catagories=bookCategory.objects.all()

    return render(request,'home.html',{"catagories":catagories})