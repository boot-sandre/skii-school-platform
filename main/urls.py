from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .api import api
from apps.skii_school_core.api import api_skii


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("skii/", api_skii.urls),
    path("", include("apps.account.urls")),
    # path("", include("apps.skii_school_core.urls")),
    re_path(r"^", TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # Turn on debug toolbar
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
