from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Note, Video
from .serializers import CategorySerializer, NoteSerializer, VideoSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related("sections__videos")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.select_related("section", "section__category")
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user).select_related(
            "video", "video__section"
        )
        video_id = self.request.query_params.get("video_id")
        if video_id:
            queryset = queryset.filter(video_id=video_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="by-video/(?P<video_id>[^/.]+)")
    def by_video(self, request, video_id=None):
        notes = self.get_queryset().filter(video_id=video_id)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)
