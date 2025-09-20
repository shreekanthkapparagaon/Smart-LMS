from django.urls import path,include
import entries.views as views



urlpatterns = [
    path("",views.log_entries , name="logs"),
    path("visit/",views.log_visit , name="logvisit"),
    # path("visit/",views.VisitCreateView.as_view({'post':'create'})),
]