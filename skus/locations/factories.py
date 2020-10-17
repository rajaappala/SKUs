import factory
from factory.django import DjangoModelFactory

from locations import models


class LocationFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: u'Location_%d' % n)
    sku_code = factory.Sequence(lambda n: u'SKU_%d' % n)
    sku_name = factory.Sequence(lambda n: u'SK_%d' % n)

    class Meta:
        model = models.Location


class DepartmentFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: u'Location_%d' % n)
    location = factory.SubFactory(LocationFactory)

    class Meta:
        model = models.Department


class CategoryFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: u'Location_%d' % n)
    department = factory.SubFactory(DepartmentFactory)

    class Meta:
        model = models.Category


class SubcategoryFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: u'Location_%d' % n)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = models.SubCategory
