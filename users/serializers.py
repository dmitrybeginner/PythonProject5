from rest_framework import serializers

from .models import Payment, User


# This serializer will be used for displaying payment details
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


# This new serializer will be used for creating a payment
class PaymentCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
