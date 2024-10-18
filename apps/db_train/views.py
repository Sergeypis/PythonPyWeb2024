from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count, Sum
from django.db import connection, reset_queries


def print_queries(*, todo: int):
    print(f"{todo}. ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    reset_queries(todo=1)


class TrainView(View):
    def get(self, request):
        # TODO 1. Какие авторы имеют самый высокий уровень самооценки (self_esteem)?
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])
        print_queries(todo=1)

        # TODO 2. Какой автор имеет наибольшее количество опубликованных статей?
        authors = Author.objects.annotate(number_of_entries=Count('entries'))
        max_entries = authors.aggregate(max_entries=Max('number_of_entries'))
        self.answer2 = authors.filter(number_of_entries=max_entries['max_entries'])
        print_queries(todo=2)

        # TODO 3. Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer3 = Entry.objects.filter(Q(tags__name='Кино') | Q(tags__name='Музыка')).distinct()
        print_queries(todo=3)

        # TODO 4. Сколько авторов женского пола зарегистрировано в системе?
        self.answer4 = Author.objects.filter(gender='ж').count()
        print_queries(todo=4)

        # TODO 5. Какой процент авторов согласился с правилами при регистрации?
        data_for_calc = Author.objects.aggregate(sum=Sum('status_rule'), total=Count('id'))
        self.answer5 = round(data_for_calc['sum']/data_for_calc['total']*100, 2)
        print_queries(todo=5)

        # TODO 6. Какие авторы имеют стаж от 1 до 5 лет?
        self.answer6 = Author.objects.filter(authorprofile__stage__range=(1, 5))
        print_queries(todo=6)

        # TODO 7. Какой автор имеет наибольший возраст?
        max_age = Author.objects.aggregate(max_age=Max('age'))
        self.answer7 = Author.objects.filter(age=max_age['max_age'])
        print_queries(todo=7)


        self.answer8 = None  # TODO 8. Сколько авторов указали свой номер телефона?
        self.answer9 = None  # TODO 9. Какие авторы имеют возраст младше 25 лет?
        self.answer10 = None  # TODO 10. Сколько статей написано каждым автором?

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}
        return render(request, 'train_db/training_db.html', context=context)

