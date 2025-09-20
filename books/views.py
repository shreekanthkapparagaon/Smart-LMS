from django.shortcuts import render
from books.models import Book,bookCategory
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json,os,joblib
# Create your views here.

current_file_path = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(current_file_path,"subject_predictor","subject_predictor_model.pkl"))
vectorizer = joblib.load(os.path.join(current_file_path,"subject_predictor","tfidf_vectorizer.pkl"))
mlb = joblib.load(os.path.join(current_file_path,"subject_predictor","subject_binarizer.pkl"))
def predict_subject(title, auther, department):
    text = f"{title} {auther}"
    vec = vectorizer.transform([text])
    pred = model.predict(vec)
    return mlb.inverse_transform(pred)[0]
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

@csrf_exempt  # Only for testing; use CSRF protection in production
def predict_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get("title")
            auther = data.get("auther")
            department = data.get("department")
            print({"title":title,"auther":auther,"department":department})
            pre = predict_subject(title=title,auther=auther,department=department)
            return JsonResponse({
                'subjects': pre
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

# @csrf_exempt
# def pridict_department(request):
#     # print("predicted")
#     # if request.method == "POST":
#     #     try:
#     #         data = json.loads(request.body)
#     #         title = data.get("title")
#     #         auther = data.get("auther")
#     #         department = data.get("department")
#     #         print({"title":title,"auther":auther,"department":department})
#     #         pre = predict_subject(title=title,auther=auther,department=department)
#     #         return JsonResponse({"department":pre[0]},status = 200)
#     #     except Exception as e:
#     #         print(e)
#     return JsonResponse({"error":"eoore"},status=200)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Shelf, bookCategory

BRANCH_ROW_MAP = {
    "CSE": 1,
    "ME": 2,
    "ECE": 3,
    "CE": 4,
    "EEE": 5
}

RACK_MATRIX = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

@api_view(['POST'])
def predict_shelf(request):
    title = request.data.get('title')
    author = request.data.get('author')
    branch = request.data.get('branch')

    if not all([title, author, branch]):
        return Response({"error": "Missing title, author, or branch"}, status=400)

    row = BRANCH_ROW_MAP.get(branch)
    if not row:
        return Response({"error": f"Unknown branch '{branch}'"}, status=400)

    for col in range(1, 8):  # C1 to C7
        for rack in RACK_MATRIX:
            addr = f"C{col}-R{row}-{rack}"
            shelf = Shelf.objects.filter(Address=addr, Quantity__lt=5).first()
            if shelf:
                return Response({
                    "predicted_shelf": shelf.Address,
                    "title": title,
                    "author": author,
                    "branch": branch
                })

    return Response({"error": "No available shelf found for this branch"}, status=404)


def books_by_branch(request, branch_code):
    books = Book.objects.filter(catagory__name=branch_code).select_related('catagory', 'addr')
    context = {
        "branch":branch_code,
        'books': books
    }
    return render(request, 'books/branch_books.html', context)
