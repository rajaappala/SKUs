import pytest

from locations import models
from locations import factories


def test_location(db, admin_user):
    factories.LocationFactory(
        sku_code="sku_1",
        sku_name="sku_name",
        name="location",
        user=admin_user
    )
    assert models.Location.objects.count() == 1
    location = models.Location.objects.first()
    assert location.name == 'location'


def test_department(db, admin_user):
    location = factories.LocationFactory(user=admin_user)
    factories.DepartmentFactory(name="test dpt", location=location, user=admin_user)

    assert models.Location.objects.count() == 1
    assert models.Department.objects.count() == 1
    dept = models.Department.objects.first()
    assert dept.name == 'test dpt'


def test_category(db, admin_user):
    location = factories.LocationFactory(user=admin_user)
    department = factories.DepartmentFactory(location=location, user=admin_user)
    factories.CategoryFactory(name="test cat", department=department, user=admin_user)

    assert models.Location.objects.count() == 1
    assert models.Department.objects.count() == 1
    assert models.Category.objects.count() == 1
    cat = models.Category.objects.first()
    assert cat.name == 'test cat'


def test_subcategory(db, admin_user):
    location = factories.LocationFactory(user=admin_user)
    department = factories.DepartmentFactory(location=location, user=admin_user)
    category = factories.CategoryFactory(department=department, user=admin_user)
    factories.SubcategoryFactory(name="test subcat", category=category, user=admin_user)

    assert models.Location.objects.count() == 1
    assert models.Department.objects.count() == 1
    assert models.Category.objects.count() == 1
    assert models.SubCategory.objects.count() == 1
    s_cat = models.SubCategory.objects.first()
    assert s_cat.name == 'test subcat'
