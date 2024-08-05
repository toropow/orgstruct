from django.test import TestCase
from orgstruct.models import Title, Department, Hierarchy, Worker
from django.test import Client
from django.urls import reverse


class TestModel(TestCase):
    def setUp(self):
        self.title = Title.objects.create(name="title 1")
        self.department_parent = Department.objects.create(name="Department 1")
        self.department = Department.objects.create(name="Department 2")
        self.worker = Worker.objects.create(
            name="Anton",
            title=self.title,
            date_employment="2015-07-11 05:55:01",
            salary_range=400000,
            department=self.department,
        )

    def tearDown(self):
        Worker.objects.all().delete()
        Title.objects.all().delete()
        Department.objects.all().delete()

    def test_model_title(self):
        self.assertEqual("title 1", str(self.title))

    def test_model_worker(self):
        self.assertEqual("Anton", str(self.worker))

    def test_model_department(self):
        self.assertEqual("Department 2", str(self.department))


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_index(self):
        url = reverse("orgstruct:hierarchy_company")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
