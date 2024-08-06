from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "orgstruct"

urlpatterns = [
    path("", views.index, name="index"),
    path("/hierarchy/", views.hierarchy_company, name="hierarchy_company"),
    path("/<int:worker_id>/", views.detail_worker, name="detail_worker"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
