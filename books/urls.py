from django.urls import path
from books import views
urlpatterns = [
    path('',views.all_books),
    path('catagories/',views.catagories_books),
    path('predict/',views.predict_view,name="sub-predict"),
]