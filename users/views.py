import stripe
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course

from .models import Payment, Subscription, User
from .serializers import (PaymentCreateSerializer, PaymentSerializer,
                          UserSerializer)
from .services import (create_stripe_price, create_stripe_product,
                       create_stripe_session)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Просмотр списка платежей с возможностью фильтрации и сортировки."
    ),
)
class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PaymentCreateSerializer,
        responses={201: PaymentSerializer, 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = serializer.validated_data["course_id"]
        course = get_object_or_404(Course, pk=course_id)

        try:
            stripe_product = create_stripe_product(course.name)
            stripe_price = create_stripe_price(stripe_product.id, course.price)
            stripe_session = create_stripe_session(stripe_price.id)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            payment_method=Payment.STRIPE,
            payment_link=stripe_session.url,
            stripe_session_id=stripe_session.id,
        )

        response_serializer = PaymentSerializer(payment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Просмотр списка пользователей."
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Просмотр одного пользователя."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание (регистрация) нового пользователя. Права доступа не требуются."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Полное обновление данных пользователя."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное обновление данных пользователя."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление пользователя."),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=(
            "Создание или удаление подписки на курс. Отправка POST-запроса на этот эндпоинт "
            "создает подписку, если ее нет, и удаляет, если она есть."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID курса для подписки/отписки",
                ),
            },
            required=["course_id"],
        ),
        responses={
            200: openapi.Response(
                description="Успешное создание или удаление подписки",
                examples={"application/json": {"message": "подписка добавлена"}},
            )
        },
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item, created = Subscription.objects.get_or_create(
            user=user, course=course_item
        )

        if not created:
            subs_item.delete()
            message = "подписка удалена"
        else:
            message = "подписка добавлена"

        return Response({"message": message})
