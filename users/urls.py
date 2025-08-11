from django.urls import path
# from users.admin import admin_site
from users import views

urlpatterns = [
    # path('cadmin/',admin_site.urls),
    # path('add-/',admin_site.urls),
    path('login/',views.loginUser),
    path('logout/',views.logoutUser),
]