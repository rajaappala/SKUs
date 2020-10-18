from rest_framework import serializers
from locations import models


class LocationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Location
        fields = ['id', 'sku_code', 'sku_name', 'name', 'user', 'last_modified']


class DepartmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    location = serializers.StringRelatedField()

    class Meta:
        model = models.Department
        fields = ['id', 'name', 'location', 'user', 'last_modified']


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    department = serializers.StringRelatedField()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'department', 'user', 'last_modified']


class SubCategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    category = serializers.StringRelatedField()

    class Meta:
        model = models.SubCategory
        fields = ['id', 'name', 'category', 'user', 'last_modified']


class InfoGraphSerilizer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField('get_location')
    department = serializers.SerializerMethodField('get_dept')
    category = serializers.SerializerMethodField('get_category')
    subcategory = serializers.SerializerMethodField('get_subcat')

    class Meta:
        model = models.SubCategory
        fields = ['subcategory', 'category', 'department', 'location']

    def get_location(self, subcategory):
        return  subcategory.category.department.location.name

    def get_dept(self, subcategory):
        return  subcategory.category.department.name

    def get_category(self, subcategory):
        return  subcategory.category.name

    def get_subcat(self, subcategory):
        return  subcategory.name