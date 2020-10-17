import pytest
import json
from django.urls import reverse, reverse_lazy

from locations import factories
from locations import models


def setup_data(admin_user):
    location = factories.LocationFactory(
        name="location", sku_code="SKU 1", sku_name="SKU Name", user=admin_user)
    department = factories.DepartmentFactory(
        name="dept", location=location, user=admin_user)
    category = factories.CategoryFactory(
        name="cat", department=department, user=admin_user)
    subcat = factories.SubcategoryFactory(
        name="subcat", category=category, user=admin_user)

def test_locations(sku_client, admin_user):
    location = factories.LocationFactory(
        sku_code="sku_1",
        sku_name="sku_name",
        name="location",
        user=admin_user
    )
    res = sku_client.get(reverse('locations:location-list'))
    assert res.status_code == 200

    payload = {
        "sku_code": "sku_2",
        "sku_name": "sku_2",
        "name": "location2"
    }
    response = sku_client.post(
        path=reverse('locations:location-list'),
        data=json.dumps(payload),
        content_type='application/json',
        follow=True
    )
    assert response.status_code == 201
    location = models.Location.objects.last()
    assert location.name == 'location2'

    response = sku_client.get(reverse('locations:location-detail', args=[location.pk]))
    assert response.status_code == 200
    assert location.name == 'location2'

    response = sku_client.delete(reverse('locations:location-detail', args=[location.pk]))
    assert response.status_code == 204
    assert models.Location.objects.count() == 1


def test_departments(sku_client, admin_user):
    location = factories.LocationFactory(user=admin_user)
    res = sku_client.get(reverse('locations:department-list'))
    assert res.status_code == 200

    payload = {
        "name": "dept 2",
        "location": location.pk
    }
    response = sku_client.post(
        path=reverse('locations:department-list'),
        data=json.dumps(payload),
        content_type='application/json',
        follow=True
    )
    assert response.status_code == 201
    dept = models.Department.objects.last()
    assert dept.name == 'dept 2'

    response = sku_client.get(reverse('locations:department-detail', args=[dept.pk]))
    assert response.status_code == 200
    assert dept.name == 'dept 2'

    response = sku_client.delete(reverse('locations:department-detail', args=[dept.pk]))
    assert response.status_code == 204
    assert models.Department.objects.count() == 0


def test_categories(sku_client, admin_user):
    location = factories.LocationFactory(user=admin_user)
    department = factories.DepartmentFactory(location=location, user=admin_user)
    res = sku_client.get(reverse('locations:category-list'))
    assert res.status_code == 200

    payload = {
        "name": "category",
        "department": department.pk
    }
    response = sku_client.post(
        path=reverse('locations:category-list'),
        data=json.dumps(payload),
        content_type='application/json',
        follow=True
    )
    assert response.status_code == 201
    category = models.Category.objects.last()
    assert category.name == 'category'

    response = sku_client.get(reverse('locations:category-detail', args=[category.pk]))
    assert response.status_code == 200
    assert category.name == 'category'

    response = sku_client.delete(reverse('locations:category-detail', args=[category.pk]))
    assert response.status_code == 204
    assert models.Category.objects.count() == 0

def test_subcategories(sku_client, admin_user):
    location = factories.LocationFactory(user=admin_user)
    department = factories.DepartmentFactory(location=location, user=admin_user)
    category = factories.CategoryFactory(department=department, user=admin_user)
    res = sku_client.get(reverse('locations:subcategory-list'))
    assert res.status_code == 200

    payload = {
        "name": "subcategory",
        "category": category.pk
    }
    response = sku_client.post(
        path=reverse('locations:subcategory-list'),
        data=json.dumps(payload),
        content_type='application/json',
        follow=True
    )
    assert response.status_code == 201
    subcategory = models.SubCategory.objects.last()
    assert subcategory.name == 'subcategory'

    response = sku_client.get(reverse('locations:subcategory-detail', args=[subcategory.pk]))
    assert response.status_code == 200
    assert subcategory.name == 'subcategory'

    response = sku_client.delete(reverse('locations:subcategory-detail', args=[subcategory.pk]))
    assert response.status_code == 204
    assert models.SubCategory.objects.count() == 0


def test_sku(sku_client, admin_user):
    setup_data(admin_user)
    url = f"{reverse('locations:sku')}?location=location&department=dept&category=cat&subcategory=subcat"
    res = sku_client.get(url)
    assert res.status_code == 200
    data = json.loads(res.content)
    assert data[0]['sku_code'] == 'SKU 1'
    assert data[0]['sku_name'] == 'SKU Name'


def test_infograph(sku_client, admin_user):
    setup_data(admin_user)
    res = sku_client.get(reverse('locations:infograph'))
    assert res.status_code == 200
    data = json.loads(res.content)
    assert data[0]['location'] == 'location'
    assert data[0]['department'] == 'dept'
    assert data[0]['category'] == 'cat'
    assert data[0]['subcategory'] == 'subcat'