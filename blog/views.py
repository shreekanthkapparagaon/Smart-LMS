from django.shortcuts import render
from blog.models import Article

# Create your views here.
def home(request):
    blogs=Article.objects.all()
    print(blogs)
    return render(request,'blogs/index.html',{"blogs":blogs})
def blog(request,id):
    blog=Article.objects.get(id=id)
    print(blog)
    return render(request,'blogs/index.html',{"blogs":blog})