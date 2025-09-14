from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    """Тест-кейс для модели подписки."""

    def setUp(self):
        """Настройка начальных данных для тестов."""
        self.user = User.objects.create(email='user@test.com', password='123')
        self.course = Course.objects.create(name='Test Course', owner=self.user)

    def test_subscribe_and_unsubscribe(self):
        """Тестирование создания и удаления подписки."""
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.pk}

        # Подписываемся
        response = self.client.post(reverse('users:subscriptions'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписываемся
        response = self.client.post(reverse('users:subscriptions'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_unauthenticated(self):
        """Тестирование создания подписки неаутентифицированным пользователем."""
        data = {'course_id': self.course.pk}
        response = self.client.post(reverse('users:subscriptions'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)