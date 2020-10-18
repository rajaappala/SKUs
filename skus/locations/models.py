from django.db import models


class Base(models.Model):
    class Meta:
        abstract = True
        ordering = ["-last_modified"]

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Location(Base):
    name = models.CharField(max_length=200, unique=True)
    sku_code = models.SlugField(max_length=64, unique=True)
    sku_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(Base):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(Base):
    name = models.CharField(max_length=200,)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubCategory(Base):
    name = models.CharField(max_length=200,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name