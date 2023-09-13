from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .api import api
from skii.endpoint.api import api_skii


urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("skii/", api_skii.urls),
    path("", include("apps.account.urls")),
    re_path(r"^", TemplateView.as_view(template_name="index.html"))
]

if settings.DEBUG:
    # Turn on debug toolbar
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
