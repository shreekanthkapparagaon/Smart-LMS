from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.apps import apps
from books.models import Book,issueBook

class CustomAdminSite(admin.AdminSite):
    site_header = "📚 Library Admin"
    site_title = "Library Dashboard"
    index_title = "Welcome to the Library Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        from collections import defaultdict

        app_sections = defaultdict(list)

        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label.title()
            model_name = model._meta.model_name
            verbose_name = model._meta.verbose_name_plural.title()
            count = model.objects.count()
            changelist_url = f"/admin/{model._meta.app_label}/{model_name}/"

            app_sections[app_label].append({
                "name": verbose_name,
                "count": count,
                "url": changelist_url,
            })
    

        context = dict(
            self.each_context(request),
            app_sections=dict(app_sections),
        )
        return TemplateResponse(request, "admin/dashboard.html", context)




custom_admin_site = CustomAdminSite("Admin-Site")