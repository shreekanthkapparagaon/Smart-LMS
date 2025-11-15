from django.shortcuts import render
from books.models import bookTag,Book,issueBook
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
# Create your views here.

def all_books(request):
    books = Book.objects.all()
    return render(request,'books/all_books.html',{"books":books})
def catagories_books(request):
    if request.method == 'GET':
        cat = request.GET.get('category', '')
        if cat != "":
            print(cat)
            catagoryInst = bookTag.objects.filter(name=cat).first()
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
    books = Book.objects.filter(catagory__name=branch_code).select_related('addr')
    context = {
        "branch":branch_code,
        'books': books
    }
    return render(request, 'books/branch_books.html', context)


@login_required
def recommend_books(request):
    user = request.user

    # Load precomputed data
    base_path = "data"
    try:
        vectorizer = joblib.load(os.path.join(base_path, "tfidf_vectorizer.pkl"))
        X_all = joblib.load(os.path.join(base_path, "tfidf_matrix.pkl"))
        df_books = pd.read_json(os.path.join(base_path, "book_metadata.json"))
    except Exception as e:
        return JsonResponse({"error": f"Recommendation data not found: {e}"}, status=500)

    # Get user's issued books
    issued = issueBook.objects.filter(user=user).select_related('book')
    if not issued.exists():
        return JsonResponse({"message": "No reading history found."})

    read_tags = [" ".join([tag.name for tag in b.book.catagory.all()]) for b in issued]
    X_read = vectorizer.transform(read_tags)
    scores = cosine_similarity(X_all, X_read).sum(axis=1)

    df_books["score"] = scores
    read_titles = {b.book.name for b in issued}
    unread = df_books[~df_books["title"].isin(read_titles)].sort_values(by="score", ascending=False)

    return JsonResponse(unread[["title", "score"]].head(10).to_dict(orient="records"), safe=False)


from books.utils.recommendation import recommend_shelf_for_book

def recommend_shelf_api(request):
    name = request.GET.get("name")
    author = request.GET.get("author")
    tag_names = request.GET.getlist("tags[]")
    tags = bookTag.objects.filter(name__in=tag_names)
    shelf = recommend_shelf_for_book(name, tags, author)
    return JsonResponse({"recommended_addr": shelf.addr if shelf else None})

