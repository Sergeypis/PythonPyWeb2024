from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.devdb2024.models import Route
from apps.devdb2024.serializers import RouteModelSerializer


class MultiDbTestMixin:
    databases = {"default", "devdb"}

class RouteModelTestCase(MultiDbTestMixin, TestCase):

    # Unit test для проверки функционировая метода __str__
    def test_str(self):
        depart = 'Челябинск'
        arrive = 'Воркута'
        distance = '555'
        expected_str = f"Маршрут: {depart} - {arrive}, {distance} км"

        obj = Route(
            depart=depart,
            arrive=arrive,
            distance=distance,
            trip_time='1 day 00:00',
            active=True)

        actual_str = str(obj)

        self.assertEqual(actual_str, expected_str, msg=f"Не работает строковое представление для модели {obj._meta.model_name}")