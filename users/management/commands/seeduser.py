from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User, Company, Part


class Command(BaseCommand):

    help = "this command tells me that he loves me"

    def handle(self, *args, **options):

        number = 30

        seeder = Seed.seeder()
        seeder.add_entity(Company, number)
        seeder.execute()
        seeder.add_entity(Part, number)
        seeder.execute()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False,})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Users created!"))


#        return super().handle(*args, **options)
