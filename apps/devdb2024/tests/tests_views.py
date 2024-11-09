import os
import django
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
#django.setup()

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.devdb2024.models import Route
from apps.devdb2024.serializers import RouteModelSerializer
import json


class MultiDbTestMixin:
    databases = {"default", "devdb"}


class RouteViewSetTestCase(MultiDbTestMixin, APITestCase):
    fixtures = ['fixt_db_test.json']

    def setUp(self):
        print("Создаём данные в БД")
        self.route1 = Route.objects.create(
                                    depart='Челябинск',
                                    arrive='Воркута',
                                    distance='555',
                                    trip_time='1 day 00:00',
                                    active=True)
        self.route2 = Route.objects.create(
                                    depart='Ямал',
                                    arrive='Магадан',
                                    distance='666',
                                    trip_time='11:45',
                                    active=True)

    def test_list_routes(self):
        print("Запуск теста test_list_routes")
        print("______________________________")

        url = reverse('devdb2024:routes-viewset-list')  # Получаем URL ссылку
        print(f"Проверяемый маршрут: {url}")
        response = self.client.get(url)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if isinstance(response.data, dict):
            if all(response.data.get(key) for key in ['results', 'next', 'count']):
                expected_data = response.data.get('results')
                next_url = response.data.get('next')
                actual_count_object = response.data.get('count')
            else:
                raise ValueError(f"Ошибка ключей словаря: {response.data.keys()}")
        elif isinstance(response.data, list):
            expected_data = response.data
            next_url = False
            actual_count_object = len(response.data)
        else:
            raise ValueError(f"Неожидаемый тип respons'a {type(response.data)}")

        while next_url:
            print(f"Проверяем постранично:")
            print(f"Проверяемый маршрут: {next_url}")
            response = self.client.get(next_url)
            print(f"Ответ от сервера: {response.status_code}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data_next_page = response.data['results']
            expected_data.extend(data_next_page)
            next_url = response.data['next']

        expected_count_objects = Route.objects.count()
        print(f"В таблице Route {expected_count_objects} значений")
        self.assertEqual(actual_count_object, expected_count_objects)

        routes = Route.objects.all()
        serializer = RouteModelSerializer(routes, many=True)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(serializer.data, expected_data)

    def test_retrieve_route(self):
        print("Запуск теста test_retrieve_route")
        print("______________________________")
        url = reverse('devdb2024:routes-viewset-detail', kwargs={'pk': self.route1.pk})  # Укажите имя URL-шаблона и параметры
        print(f"Проверяемы маршрут: {url}")
        response = self.client.get(url)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        route = Route.objects.get(pk=self.route1.pk)
        serializer = RouteModelSerializer(route)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_create_route(self):
        print("Запуск теста test_create_route")
        print("______________________________")
        url = reverse('devdb2024:routes-viewset-list')  # Получаем URL ссылку
        print(f"Проверяемы маршрут: {url}")
        data = {
                'depart': 'Магадан',
                'arrive': 'Ямал',
                'distance': 670,
                'trip_time': '12:30',
                'active': True
        }
        response = self.client.post(url, data)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        route = Route.objects.get(depart='Магадан', arrive='Ямал', distance=670)
        serializer = RouteModelSerializer(route)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_update_route(self):
        print("Запуск теста test_update_route")
        print("______________________________")
        url = reverse('devdb2024:routes-viewset-detail', kwargs={'pk': self.route1.pk})
        print(f"Проверяемы маршрут: {url}")
        data = {
                'depart': 'Магадан',
                'arrive': 'Ямал',
                'distance': 700,
                'trip_time': '14:30',
                'active': True
        }
        response = self.client.put(url, data)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        route = Route.objects.get(pk=self.route1.pk)
        serializer = RouteModelSerializer(route)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_route(self):
        print("Запуск теста test_partial_update_route")
        print("______________________________")
        url = reverse('devdb2024:routes-viewset-detail', kwargs={'pk': self.route1.pk})
        print(f"Проверяемы маршрут: {url}")
        data = {
                'depart': 'Магадан',
                'arrive': 'Ямал',
                'distance': 700,
                'trip_time': '14:30',
                'active': True
        }
        response = self.client.patch(url, data)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        route = Route.objects.get(pk=self.route1.pk)
        serializer = RouteModelSerializer(route)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_delete_route(self):
        print("Запуск теста test_delete_route")
        print("______________________________")
        url = reverse('devdb2024:routes-viewset-detail', kwargs={'pk': self.route1.pk})
        print(f"Проверяемы маршрут: {url}")
        response = self.client.delete(url)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Route.objects.filter(pk=self.route1.pk).exists())  # Проверка, что теперь этого автора не существует

class ViewsAPITestCase(MultiDbTestMixin, APITestCase):

    def test_empty_lists_response(self):
        url = reverse('devdb2024:routes-viewset-list')
        response = self.client.get(url)
        if isinstance(response.data, dict):
            data = response.data['results']
        elif isinstance(response.data, list):
            data = response.data
        else:
            raise ValueError(f"Неожидаемый тип respons'a {type(response.data)}")

        self.assertIsInstance(data, list, msg="Должен быть тип list")
        self.assertEqual(0, len(data), msg="Должен быть пустой список")
