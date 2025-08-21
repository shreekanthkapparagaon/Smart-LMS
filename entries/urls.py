from django.urls import path
import entries.views as views

urlpatterns = [
    path("",views.log_entries , name="logs"),
    path("visit/",views.log_visit , name="logvisit"),
    # path('create-resource/', MyResourceCreateView.as_view(), name='create-resource'),
]