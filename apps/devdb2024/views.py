# from Tools.scripts.patchcheck import status
from functools import partial
from venv import create

from django.db.migrations import CreateModel
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404
from django.views import View
from rest_framework.viewsets import ViewSet, ModelViewSet

from .serializers import RouteSerializer, RouteModelSerializer

from django.views.decorators.csrf import csrf_exempt
import json

from apps.devdb2024.models import Route


class DevDBRouteREST(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, id=None):

        if id is None:  # Проверяем, что требуется вернуть всех пользователей
            data = []
            for route in Route.objects.all():
                data_route = {'id': route.route_id,
                    'depart': route.depart,
                    'arrive': route.arrive,
                    'trip_time': route.trip_time}
            data.append(data_route)

        else:
            if route := Route.objects.get(route_id=id):  # Нужен обработчик исключений!!!
                data = {'id': route.route_id,
                    'depart': route.depart,
                    'arrive': route.arrive,
                    'trip_time': route.trip_time}
            else:
                return JsonResponse({'error': f'Автора с id={id} не найдено!'},
                                    status=404,
                                    json_dumps_params={"ensure_ascii": False,
                                                       "indent": 4}
                                    )

        return JsonResponse(data, safe=False, json_dumps_params={"ensure_ascii": False,
                                                                 "indent": 4})

    def post(self, request):
        try:
            data = json.loads(request.body)

            # route = Route.objects.create(
            #     depart=data['depart'],
            #     arrive=data['arrive'],
            #     distance=data['distance'],
            #     trip_time=data['trip_time'],
            # )
            route = Route(
                depart=data['depart'],
                arrive=data['arrive'],
                distance=data['distance'],
                trip_time=data['trip_time'],
            )
            route.clean_fields()
            route.save(using="devdb")

            response_data = {
                'message': f'Route is create',
                'route_id': route.route_id,
                'depart': route.depart,
                'arrive': route.arrive,
                'distance': route.distance,
                'trip_time': route.trip_time,
                'active': route.active,
            }

            return JsonResponse(response_data, status=201,
                                json_dumps_params={"ensure_ascii": False,
                                                    "indent": 4}
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4}
                                )

    def put(self, request, id):
        try:
            data = json.loads(request.body)
            route = Route.objects.get(pk=id)

            route.depart = data['depart']
            route.arrive = data['arrive']
            route.distance = data['distance']
            route.trip_time = data['trip_time']

            route.clean_fields()
            route.save()

            data_response = {
                    'message': 'data uodate is complete',
                    'id': route.route_id,
                    'depart': route.depart,
                    'arrive': route.arrive,
                    'distance': route.distance,
                    'trip_time': route.trip_time
            }

            return JsonResponse(data_response,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})
        except Route.DoesNotExist:
            return JsonResponse({"error": "this route not exists"}, status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})

    def patch(self, request, id):
        try:
            data = json.loads(request.body)
            route = Route.objects.get(pk=id)

            for key, value in data.items():
                setattr(route, key, value)

            route.clean_fields()
            route.save()

            data_response = {
                'message': 'data uodate is complete',
                'id': route.route_id,
                'depart': route.depart,
                'arrive': route.arrive,
                'distance': route.distance,
                'trip_time': route.trip_time
            }

            return JsonResponse(data_response,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})
        except Route.DoesNotExist:
            return JsonResponse({"error": "this route not exists"}, status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})

    def delete(self, request, id):
        try:
            route = Route.objects.get(pk=id)
            route.delete()

            return JsonResponse({"message":" Маршрут успешно удалён"},
                                json_dumps_params={"ensure_ascii": False,
                                                  "indent": 4})
        except Route.DoesNotExist:
            return JsonResponse({"error": "this route not exists"}, status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4})

class RouteAPIView(APIView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, id=None):
        if id is not None:
            try:
                route = Route.objects.get(pk=id)
                serializer = RouteModelSerializer(route)
                return Response(serializer.data)
            except Route.DoesNotExist:
                return Response({"message": "Маршрут не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            routes = Route.objects.all()
            serializer = RouteModelSerializer(routes, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = RouteModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            route = Route.objects.get(pk=id)
        except Route.DoesNotExist:
            return Response({"message": "Маршрут не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RouteModelSerializer(route, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            route = Route.objects.get(pk=id)
        except Route.DoesNotExist:
            return Response({"message": "Маршрут не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RouteModelSerializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            route = Route.objects.get(pk=id)
        except Route.DoesNotExist:
            return Response({"message": "Маршрут не найден"}, status=status.HTTP_404_NOT_FOUND)

        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RouteGenericAPIView(GenericAPIView, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin):
    queryset = Route.objects.all()
    serializer_class = RouteModelSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get(self.lookup_field):
            try:
                return self.retrieve(request, *args, **kwargs)
            except Http404:
                return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except Http404:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The object has been deleted"}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except Http404:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

class RoutePagination(PageNumberPagination):
    page_size = 5  # количество объектов на странице
    page_size_query_param = 'page_size'  # параметр запроса для настройки количества объектов на странице
    max_page_size = 1000  # максимальное количество объектов на странице

class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteModelSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # Ограничение методов представления(по умолчанию все активны)
    pagination_class = RoutePagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['depart', 'arrive']  # Указываем для каких полем можем проводить фильтрацию
    search_fields = ['depart', 'arrive']  # Поля, по которым будет выполняться поиск
    ordering_fields = ['trip_time']  # Поля, по которым можно сортировать

    # Переопределение метода get_queryset() для фильтрации по query_params
    def get_queryset(self):
        queryset = super().get_queryset()
        depart = self.request.query_params.get('depart')
        if depart:
            queryset = queryset.filter(depart__icontains=depart)
        return queryset

    # написание пользовательский действий, т.е. методов (которые не вписываются в стандартные операции CRUD),
    # которые будут вызываться при заходе на определенный путь: /<pk>/my_action/
    @action(detail=True, methods=['get'])
    def my_action(self, request, pk=None):
        # Ваша пользовательская логика здесь
        return Response({'message': f'Пользовательская функция для пользователя с pk={pk}'})
