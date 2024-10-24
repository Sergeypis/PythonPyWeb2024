from django.urls import path
from . views import DevDBREST


urlpatterns = [
    path('devdb/', DevDBREST.as_view()),
    path('devdb/<int:id>/', DevDBREST.as_view()),
]