from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    """Тест-кейс для модели урока."""

    def setUp(self):
        """Настройка начальных данных для тестов."""
        self.user = User.objects.create(email="user@test.com", password="123")
        self.moderator_group = Group.objects.create(name="moderator")
        self.moderator = User.objects.create(email="moderator@test.com", password="123")
        self.moderator.groups.add(self.moderator_group)

        self.course = Course.objects.create(name="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=test",
        )

    def test_create_lesson(self):
        """Тестирование создания урока."""
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "New Lesson",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/watch?v=new",
        }
        response = self.client.post(reverse("lms:lessons-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_by_moderator_forbidden(self):
        """Тестирование запрета создания урока модератором."""
        self.client.force_authenticate(user=self.moderator)
        data = {"name": "New Lesson", "course": self.course.pk}
        response = self.client.post(reverse("lms:lessons-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lessons(self):
        """Тестирование получения списка уроков."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("lms:lessons-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_lessons_by_moderator(self):
        """Тестирование получения списка уроков модератором."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(reverse("lms:lessons-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Should see all lessons

    def test_retrieve_lesson_by_owner(self):
        """Тестирование получения урока владельцем."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("lms:lessons-detail", kwargs={"pk": self.lesson.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    def test_retrieve_lesson_by_moderator(self):
        """Тестирование получения урока модератором."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(
            reverse("lms:lessons-detail", kwargs={"pk": self.lesson.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    def test_update_lesson_by_owner(self):
        """Тестирование обновления урока владельцем."""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Updated Lesson Name"}
        response = self.client.patch(
            reverse("lms:lessons-detail", kwargs={"pk": self.lesson.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated Lesson Name")

    def test_update_lesson_by_moderator(self):
        """Тестирование обновления урока модератором."""
        self.client.force_authenticate(user=self.moderator)
        data = {"name": "Updated by Moderator"}
        response = self.client.patch(
            reverse("lms:lessons-detail", kwargs={"pk": self.lesson.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated by Moderator")

    def test_delete_lesson_by_owner(self):
        """Тестирование удаления урока владельцем."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("lms:lessons-detail", kwargs={"pk": self.lesson.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_by_moderator_forbidden(self):
        """Тестирование запрета удаления урока модератором."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(
            reverse("lms:lessons-detail", kwargs={"pk": self.lesson.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_video_link_validator(self):
        """Тестирование валидатора ссылки на видео в уроке."""
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Lesson with bad link",
            "course": self.course.pk,
            "video_link": "https://www.my-bad-site.com/",
        }
        response = self.client.post(reverse("lms:lessons-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_link", response.data)
