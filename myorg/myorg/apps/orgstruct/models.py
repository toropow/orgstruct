from django.db import models


class Hierarchy(models.Model):
    data = models.JSONField()
    ttl = models.DateTimeField(auto_now_add=True)


class Title(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50, null=False)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, related_name="department_level_up")

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=50, null=False)
    title = models.ForeignKey(Title, null=False, on_delete=models.PROTECT)
    date_employment = models.DateField(null=False)
    salary_range = models.DecimalField(max_digits=8, decimal_places=2)
    department = models.ForeignKey(Department, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
