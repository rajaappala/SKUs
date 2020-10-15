from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.decorators import action
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


class CategoryViewSet(BaseViewSet):
    """
    This viewset provides `CRUD` actions for Category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(BaseViewSet):
    """
    This viewset provides `CRUD` actions for SubCategory
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SKU(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    This is to get all the SKUs with location, dept, category and subcategory
    """
    queryset = Location.objects.all()

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


class InfoGraph(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    This is to get all the SKUs with location, dept, category and subcategory
    """
    queryset = SubCategory.objects.all()
    serializer_class = InfoGraphSerilizer

    def get(self, request, *args, **kwargs):
        graph_data = [self.get_serializer(item).data for item in self.get_queryset()]
        return Response(graph_data)
