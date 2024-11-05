from django.urls import path, include
from rest_framework.routers import DefaultRouter
from setuptools.extern import names

from .views import DevDBRouteREST, RouteAPIView, RouteGenericAPIView, RouteViewSet
from ..api.urls import app_name

app_name = 'devdb2024'

router = DefaultRouter()
router.register(r'routes_viewset', RouteViewSet, basename='routes-viewset')

urlpatterns = [
    path('devdb/route/', DevDBRouteREST.as_view()),
    path('devdb/route/<int:id>/', DevDBRouteREST.as_view()),
    path('api/devdb/route/', RouteAPIView.as_view(), name='routes-list'),
    path('api/devdb/route/<int:id>/', RouteAPIView.as_view(), name='route-details'),
    path('routes_generic/', RouteGenericAPIView.as_view(), name='route-generic-list'),
    path('routes_generic/<int:pk>/', RouteGenericAPIView.as_view(), name='route-generic-detail'),
    path('', include(router.urls))
]