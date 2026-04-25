from rest_framework import serializers

from .models import Category, Note, Section, Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "title", "url", "section"]


class SectionSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ["id", "name", "category", "videos"]


class CategorySerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "sections"]


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "user", "video", "content", "timestamp", "updated_at"]
        read_only_fields = ["id", "user", "updated_at"]
