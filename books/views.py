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
