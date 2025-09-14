from rest_framework import viewsets
from .models import Course, Lesson
from .paginators import CoursePaginator, LessonPaginator
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели курсов."""
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet для модели уроков."""
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['update', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
