# from Tools.scripts.patchcheck import status
from django.http import JsonResponse
from django.views import View

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
            for route in Route.objects.all().using("devdb"):
                data_route = {'id': route.route_id,
                    'depart': route.depart,
                    'arrive': route.arrive,
                    'trip_time': route.trip_time}
            data.append(data_route)

        else:
            if route := Route.objects.using("devdb").get(route_id=id):
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



