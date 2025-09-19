from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from core import views

urlpatterns = [
    path("", views.home , name="home"),
    path('schema-viewer/', include('schema_viewer.urls')),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path("blog/", include("blog.urls")),
    path("books/", include("books.urls")),
    path("log-entries/", include("entries.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
