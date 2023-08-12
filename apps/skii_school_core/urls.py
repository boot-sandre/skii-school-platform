from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .api import api_skii

urlpatterns = [
    path("skii-school-core/", api_skii.urls),
]
