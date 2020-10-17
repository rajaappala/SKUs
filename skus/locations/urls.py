from django.urls import path, include
from locations import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'location', views.LocationViewSet, basename='location')
router.register(r'department', views.DepartmentViewSet, basename='department')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'subcategory', views.SubCategoryViewSet, basename='subcategory')

urlpatterns = [
    path('', include(router.urls)),
    path('sku', views.SKU.as_view(), name='sku'),
    path('infograph', views.InfoGraph.as_view(), name='infograph')
]
