from django.core.management.base import BaseCommand
from users.models import User, Payment
from lms.models import Course, Lesson

class Command(BaseCommand):
    help = 'Seeds the database with initial payment data.'

    def handle(self, *args, **kwargs):
        # Start by clearing all existing payments to avoid duplicates
        self.stdout.write("Deleting existing payment data...")
        Payment.objects.all().delete()

        # Get or create a user to associate payments with
        user, created = User.objects.get_or_create(
            email='testuser@example.com',
            defaults={'first_name': 'Test', 'last_name': 'User'}
        )
        if created:
            user.set_password('password')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User already exists: {user.email}'))

        # Get or create a course and a lesson
        course, created = Course.objects.get_or_create(name='Django for Beginners')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created course: {course.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course.name}'))

        lesson, created = Lesson.objects.get_or_create(name='Introduction to Models', course=course)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created lesson: {lesson.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Lesson already exists: {lesson.name}'))

        # Create payment records
        payments_to_create = [
            {
                'user': user,
                'paid_course': course,
                'amount': 15000,
                'payment_method': Payment.TRANSFER,
            },
            {
                'user': user,
                'paid_lesson': lesson,
                'amount': 700,
                'payment_method': Payment.CASH,
            },
            {
                'user': user,
                'paid_course': course,
                'amount': 14500,
                'payment_method': Payment.TRANSFER,
            },
        ]

        for payment_data in payments_to_create:
            payment = Payment.objects.create(**payment_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created payment: {payment}'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))
