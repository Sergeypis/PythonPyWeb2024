from django.urls import path
from . views import DevDBRouteREST


urlpatterns = [
    path('devdb/route/', DevDBRouteREST.as_view()),
    path('devdb/route/<int:id>/', DevDBRouteREST.as_view()),
]