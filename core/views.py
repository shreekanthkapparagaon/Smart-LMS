from django.shortcuts import render
# from blog.models import Article
from books.models import Book
from django.db.models import Count
from books.views import recommend_books
import json


# Create your views here.
def home(request):
    catagories = (
    Book.objects
    .annotate(issue_count=Count('issuebook'))
    .filter(issue_count__gt=0)
    .order_by('-issue_count')[:10]
)
    response = recommend_books(request)

    try:
        recomendded_books = json.loads(response.content)
    except Exception as e:
        recomendded_books = []
        print(f"Error parsing recommendations: {e}")

    # column_values = MyModel.objects.values_list('my_column', flat=True) 
    return render(request,'home.html',{"catagories":catagories,"recomended_books":recomendded_books})
