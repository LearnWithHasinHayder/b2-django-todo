from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a custom permission'

    def handle(self, *args, **options):
        # Get the content type for the User model
        content_type = ContentType.objects.get_for_model(User)

        # Create the permission
        permission, created = Permission.objects.get_or_create(
            codename='custom_permission',
            name='Custom Permission',
            content_type=content_type,
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created custom permission'))
        else:
            self.stdout.write(self.style.WARNING('Permission already exists'))