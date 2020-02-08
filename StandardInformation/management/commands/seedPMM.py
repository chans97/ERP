from django.core.management.base import BaseCommand
from django_seed import Seed
from StandardInformation.models import Partner, Material, SupplyPartner, SingleProduct, SingleProductMaterial, Measure
from users import models
import random


class Command(BaseCommand):

    help = "this command tells me that he loves me"

    def handle(self, *args, **options):

        number = 4
        seeder = Seed.seeder()
        all_supplier = SupplyPartner.objects.all()
        자재품명 = ["볼트", "너트", "전선", "버튼"]
        거래처구분 = ["공급처", "대리점", "고객"]
        all_user = models.User.objects.all()
        seeder.add_entity(
            Partner,
            number,
            {
                "작성자": lambda x: random.choice(all_user),
                "담당자": lambda x: random.choice(all_user),
                "거래처구분" : lambda x: random.choice(거래처구분),
            },
        )
        seeder.execute()


        seeder.add_entity(
            Material,
            number,
            {
                "자재공급업체": lambda x: random.choice(all_supplier),
                "자재품명": lambda x: random.choice(자재품명),
            },
        )
        seeder.execute()

        seeder.add_entity(
            Measure,
            number,
        )
        seeder.execute()




        self.stdout.write(self.style.SUCCESS(f"{number} SI created!"))


#        return super().handle(*args, **options)
