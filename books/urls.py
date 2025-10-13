from django.urls import path
from books import views
urlpatterns = [
    path('',views.all_books),
    path('catagories/',views.catagories_books),
    path('<str:branch_code>/',views.books_by_branch, name='books-by-branch'),

]