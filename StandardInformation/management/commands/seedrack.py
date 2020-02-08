import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import User
from StandardInformation.models import SingleProductMaterial, Material, SingleProduct, RackProductMaterial, RackProduct


class Command(BaseCommand):

    help = "this command tells me that he loves me"

    def handle(self, *args, **options):
        number = 3
        seeder = Seed.seeder()
        all_number = [1,2,3,4,5,6,7,8,9,10]
        all_user = User.objects.all()

        seeder.add_entity(RackProduct, number,
                    {"작성자" : lambda x: random.choice(all_user),
            },)
        seeder.execute()


        
        all_rack = RackProduct.objects.all()
        seeder.add_entity(RackProductMaterial, number,
                    {"랙모델" : lambda x: random.choice(all_rack),
                "수량": lambda x: random.choice(all_number),
            },)
        created_phtos = seeder.execute()
        created_clean = list(created_phtos.values())[1]
        singleproduct = SingleProduct.objects.all()

        for pk in created_clean:
            sm = RackProductMaterial.objects.get(pk=pk)
            m = random.choice(singleproduct)
            sm.랙구성단품.add(m)

        self.stdout.write(self.style.SUCCESS(f"{number} RM created!"))
