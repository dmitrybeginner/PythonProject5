from rest_framework import serializers
from .models import Course, Lesson
from .validators import youtube_link_validator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'preview', 'video_link', 'course', 'owner')
        extra_kwargs = {
            'video_link': {'validators': [youtube_link_validator]}
        }


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'lessons_count', 'lessons', 'is_subscribed')
