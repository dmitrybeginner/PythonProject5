from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.get_or_create(name='moderator')
        self.stdout.write(self.style.SUCCESS('Successfully created moderator group'))
