from rest_framework import viewsets, permissions, status, generics, mixins
from django.db.models import F
from rest_framework.response import Response

from locations.models import *
from locations.serializers import *
import logging

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ModelViewSet):
    """
    This is a base viewset to provides `CRUD` actions
    """
    queryset = None
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        logger.info(f"Creating record to table {serializer.Meta.model._meta.label}"
                    f" by {self.request.user}")
        serializer.save(user=self.request.user)


class LocationViewSet(BaseViewSet):
    """
    This viewset provides `CRUD` actions for location
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DepartmentViewSet(BaseViewSet):
    """
    This viewset provides `CRUD` actions for Department
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        locations = Location.objects.values(value=F('id'), text=F('name')).order_by('name')
        response = {
            "locations": locations
        }
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response['departments'] = serializer.data
            return self.get_paginated_response(response)

        serializer = self.get_serializer(queryset, many=True)
        response['departments'] = serializer.data
        return Response(response)


class CategoryViewSet(BaseViewSet):
    """
    This viewset provides `CRUD` actions for Category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        departments = Department.objects.values(value=F('id'), text=F('name')).order_by('name')
        response = {
            "departments": departments
        }
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response['categories'] = serializer.data
            return self.get_paginated_response(response)

        serializer = self.get_serializer(queryset, many=True)
        response['categories'] = serializer.data
        return Response(response)


class SubCategoryViewSet(BaseViewSet):
    """
    This viewset provides `CRUD` actions for SubCategory
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        categories = Category.objects.values(value=F('id'), text=F('name')).order_by('name')
        response = {
            "categories": categories
        }
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response['subcategories'] = serializer.data
            return self.get_paginated_response(response)

        serializer = self.get_serializer(queryset, many=True)
        response['subcategories'] = serializer.data
        return Response(response)


class SKU(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    This is to get all the SKUs with location, dept, category and subcategory
    """
    queryset = Location.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        location = request.GET.get('location', None)
        dept = request.GET.get('department', None)
        category = request.GET.get('category', None)
        subcategory = request.GET.get('subcategory', None)
        if all([location, dept, category, subcategory]):
            logger.info(f"fetching SKUs for location: {location}, "
                        f"department: {dept}, category: {category}, subcat:{subcategory}")
            sku_data = self.queryset.filter(
                name=location,
                department__name=dept,
                department__category__name=category,
                department__category__subcategory__name=subcategory
            ).values('sku_code', 'sku_name')
            return Response(sku_data)
        else:
            logger.error(f"Invalid request data by user: {self.request.user}")
            return Response('Please provide all arguments', status=status.HTTP_400_BAD_REQUEST)


class InfoGraphViewset(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    This is to get all the SKUs with location, dept, category and subcategory
    """
    queryset = Location.objects.all()
    serializer_class = LocationGraphSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        locations = self.queryset.values(value=F('id'), text=F('name')).order_by('name')
        return Response(locations)

    def retrieve(self, request, *args, **kwargs):
        location = self.get_object()
        logger.info(f"Fetching the relation tree of the location: {location.name}")
        location_data = self.get_serializer(location).data
        departments = Department.objects.filter(id__in=location_data['department_set'])
        location_data['children'] = []
        del location_data['department_set']
        for department in departments:
            dept_data = DepartmentGraphSerializer(department).data
            categories = Category.objects.filter(id__in=dept_data['category_set'])
            dept_data['children'] = []
            del dept_data['category_set']
            for category in categories:
                cat_data = CategoryGraphSerializer(category).data
                subcat_list = list(SubCategory.objects.filter(id__in=cat_data['subcategory_set']).values('name'))
                cat_data['children'] = subcat_list
                del cat_data['subcategory_set']
                dept_data['children'].append(cat_data)
            location_data['children'].append(dept_data)

        return Response(location_data)
