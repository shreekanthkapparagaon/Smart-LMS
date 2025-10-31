from django.urls import path
from books import views
urlpatterns = [
    path('',views.all_books),
    path("api/recommend-shelf/", views.recommend_shelf_api, name="recommend_shelf_api"),

    path('catagories/',views.catagories_books),
    path("recommend/", views.recommend_books),
    path('<str:branch_code>/',views.books_by_branch, name='books-by-branch'),
]