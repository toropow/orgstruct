from django.core.management.base import BaseCommand, CommandError
from orgstruct.models import Title, Department, Worker
from django.contrib.auth.models import User
import factory
from random import randint
from datetime import timedelta


class WorkerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Worker

    department = factory.Iterator(Department.objects.all())
    title = factory.Iterator(Title.objects.all())
    date_employment = factory.Faker("date")
    salary_range = factory.Iterator([float(randint(1000, 100000)) for x in range(100)])
    name = factory.Faker("name")


def delete_all():
    Worker.objects.all().delete()
    Title.objects.all().delete()
    Department.objects.all().delete()


class Command(BaseCommand):
    help = "Upload data"

    def handle(self, *args, **kwargs):
        titles = ["Программист", "QA", "Аналитик", "Product owner", "Data Engineer"]
        departments = [f"department_{i}_lvl_{l}" for i in range(1, 6) for l in range(5, -1, -1)]
        user_range = 50_000
        level_max = 5
        departments_obj = []

        print("------ delete old data")
        delete_all()

        print("------ upload titles")
        for title in titles:
            Title.objects.create(name=title)

        print("------ upload departments")

        for department in departments:
            departments_obj.append(Department.objects.create(name=department))

        print("------ make hierarchy.html")

        level_curr = 1
        for i in range(len(departments_obj)):
            if level_curr != level_max:
                departments_obj[i].parent = departments_obj[i + 1]
                departments_obj[i].save()

            if level_curr < level_max:
                level_curr += 1
            else:
                level_curr = 1

        print("------ upload users")

        WorkerFactory.create_batch(user_range)
