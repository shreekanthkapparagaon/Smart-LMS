from django.urls import path
from blog import views
urlpatterns = [
    # path('cadmin/',),
    path('',views.home),
    path('<int:id>',views.blog),
]