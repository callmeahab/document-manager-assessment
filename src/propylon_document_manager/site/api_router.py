from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter, SimpleRouter

from propylon_document_manager.file_versions.api.views import FileVersionViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("file_versions", FileVersionViewSet)

app_name = "api"

urlpatterns = router.urls
urlpatterns = urlpatterns + [
    path("file_versions/<path:file_path>", FileVersionViewSet.as_view({"get": "get_file"})),
]
