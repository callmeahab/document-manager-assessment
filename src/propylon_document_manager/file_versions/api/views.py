from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import FileVersion
from .serializers import FileVersionSerializer
from ..permissions import IsOwner


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(methods=["get"], detail=False, url_path="file_versions")
    def get_file(self, request, *args, **kwargs):
        print(request.path)
        file_path = request.path.replace("/api/file_versions/", "")
        print(file_path)
        version_number = 0
        if request.query_params["revision"]:
            version_number = request.query_params["revision"]
        file = self.queryset.filter(path=file_path, version_number=version_number).first()
        if file is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        content_type = file.content_type if file and file.content_type else "application/octet-stream"
        return HttpResponse(file.uploaded_file, content_type=content_type, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        file_path = request.headers["X-File-Path"]
        version_number = 0
        existing_file = self.queryset.filter(path=file_path).order_by("-version_number").first()
        uploaded_file = request.data["file"]
        if existing_file:
            version_number = existing_file.version_number + 1
        data = {
            "uploaded_file": uploaded_file,
            "content_type": uploaded_file.content_type,
            "path": file_path,
            "file_name": request.data["file"].name,
            "version_number": version_number,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
