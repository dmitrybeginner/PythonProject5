from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .paginators import CoursePaginator, LessonPaginator
from .serializers import CourseSerializer, LessonSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description=(
            "Просмотр списка курсов. Модераторы видят все курсы, "
            "остальные пользователи - только свои."
        )
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Просмотр одного курса. Доступно модераторам и владельцу курса."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description=(
            "Создание нового курса. Доступно всем аутентифицированным "
            "пользователям, кроме модераторов."
        )
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Полное обновление курса. Доступно модераторам и владельцу курса."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное обновление курса. Доступно модераторам и владельцу курса."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление курса. Доступно только владельцу курса."
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели курсов."""

    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Course.objects.none()  # Schema generation, return empty queryset
        if self.request.user.groups.filter(name="moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description=(
            "Просмотр списка уроков. Модераторы видят все уроки, "
            "остальные пользователи - только свои."
        )
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Просмотр одного урока. Доступно модераторам и владельцу урока."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description=(
            "Создание нового урока. Доступно всем аутентифицированным "
            "пользователям, кроме модераторов."
        )
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Полное обновление урока. Доступно модераторам и владельцу урока."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное обновление урока. Доступно модераторам и владельцу урока."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление урока. Доступно только владельцу урока."
    ),
)
class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet для модели уроков."""

    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Lesson.objects.none()  # Schema generation, return empty queryset
        if self.request.user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

