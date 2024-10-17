from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count


class TrainView(View):
    def get(self, request):
        # TODO Какие авторы имеют самый высокий уровень самооценки (self_esteem)?
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])

        # TODO Какой автор имеет наибольшее количество опубликованных статей?
        authors = Author.objects.annotate(number_of_entries=Count('entries'))
        max_entries = authors.aggregate(max_entries=Max('number_of_entries'))
        self.answer2 = authors.filter(number_of_entries=max_entries['max_entries'])

        # TODO Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer3 = None

        self.answer4 = None  # TODO Сколько авторов женского пола зарегистрировано в системе?
        self.answer5 = None  # TODO Какой процент авторов согласился с правилами при регистрации?
        self.answer6 = None  # TODO Какие авторы имеют стаж от 1 до 5 лет?
        self.answer7 = None  # TODO Какой автор имеет наибольший возраст?
        self.answer8 = None  # TODO Сколько авторов указали свой номер телефона?
        self.answer9 = None  # TODO Какие авторы имеют возраст младше 25 лет?
        self.answer10 = None  # TODO Сколько статей написано каждым автором?

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}
        return render(request, 'train_db/training_db.html', context=context)

