from rest_framework import serializers
from locations import models


class ISODateField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime("%m/%d/%Y, %H:%M:%S")


class LocationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    last_modified = ISODateField(read_only=True)

    class Meta:
        model = models.Location
        fields = ['id', 'sku_code', 'sku_name', 'name', 'user', 'last_modified']


class DepartmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    last_modified = ISODateField(read_only=True)

    class Meta:
        model = models.Department
        fields = ['id', 'name', 'location', 'user', 'last_modified']


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    last_modified = ISODateField(read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'department', 'user', 'last_modified']


class SubCategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    last_modified = ISODateField(read_only=True)

    class Meta:
        model = models.SubCategory
        fields = ['id', 'name', 'category', 'user', 'last_modified']


class CategoryGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['subcategory_set', 'name']


class DepartmentGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = ['category_set', 'name']


class LocationGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ['department_set', 'name']
