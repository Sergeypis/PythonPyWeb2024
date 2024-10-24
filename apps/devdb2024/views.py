from django.http import JsonResponse
from django.views import View
#from .models import Author
from django.views.decorators.csrf import csrf_exempt
import json


class DevDBREST(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, id=None):

        if id is None:  # Проверяем, что требуется вернуть всех пользователей
            data = []
            data_author = {'id': 1,
                'name': 'author.name',
                'email': 'author.email'}
            data.append(data_author)

        else:  # Иначе, так как автор не найден (QuerySet пустой), то возвращаем ошибку, с произвольным текстом,
            # для понимания почему произошла ошибка
            return JsonResponse({'error': f'Автора с id={id} не найдено!'},
                                status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4}
                                )

        # После того как данные для ответа созданы - возвращаем Json объект с данными
        return JsonResponse(data, safe=False, json_dumps_params={"ensure_ascii": False,
                                                                 "indent": 4})
