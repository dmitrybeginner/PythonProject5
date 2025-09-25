from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.get_or_create(name="moderator")
        self.stdout.write(self.style.SUCCESS("Successfully created moderator group"))
