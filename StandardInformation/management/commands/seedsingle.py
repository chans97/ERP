import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import User
from StandardInformation.models import SingleProductMaterial, Material, SingleProduct


class Command(BaseCommand):

    help = "this command tells me that he loves me"

    def handle(self, *args, **options):
        number = 3
        seeder = Seed.seeder()
        all_number = [1,2,3,4,5,6,7,8,9,10]
        all_user = User.objects.all()

        seeder.add_entity(SingleProduct, number,
                    {"작성자" : lambda x: random.choice(all_user),
            },)
        seeder.execute()


        
        all_single = SingleProduct.objects.all()
        seeder.add_entity(SingleProductMaterial, number,
                    {"단품모델" : lambda x: random.choice(all_single),
                "수량": lambda x: random.choice(all_number),
            },)
        created_phtos = seeder.execute()
        created_clean = list(created_phtos.values())[1]
        material = Material.objects.all()

        for pk in created_clean:
            sm = SingleProductMaterial.objects.get(pk=pk)
            m = random.choice(material)
            sm.단품구성자재.add(m)

        self.stdout.write(self.style.SUCCESS(f"{number} SM created!"))
