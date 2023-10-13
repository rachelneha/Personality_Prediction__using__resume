from django.core.management import BaseCommand

from manger.models import Resume


class Command(BaseCommand):

    def handle(self, *args, **options):
        r: Resume = Resume.objects.all()[0]
        print(r.get_traits)

