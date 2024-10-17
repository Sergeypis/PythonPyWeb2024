import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # 1. Вывести все записи блогов, где у автора в имени содержится 'author'
    obj = Entry.objects.filter(author__name__contains='author')
    print("1 ", obj)

    # 2. Вывести все записи блогов, где у автора не указан город
    obj = Entry.objects.filter(author__authorprofile__city=None)
    print("2 ", obj)

    # 3. Вывести все записи блогов с тэгом Фитнес
    obj = Entry.objects.filter(tags__name='Фитнес')
    print("3 ", obj)

    # 4. Точное совпадение c учетом и без учёта (работает не во всех БД) регистра соответственно (exact, iexact)
    print("4 ", Entry.objects.get(id__exact=4))
    print("4 ", Entry.objects.get(id=4))  # Аналогично exact
    print("4 ", Blog.objects.get(name__iexact="Путешествия по миру"))

    # 5. Чувствительный, нечувствительное к регистру поиск (contains, icontains)
    print("5 ", Entry.objects.filter(headline__contains='мод'))

    # 6. Проверка вхождения (in)
    print("6 ", Entry.objects.filter(id__in=[1, 3, 4]))
    print("6 ", Entry.objects.filter(number_of_comments__in='123'))  # число комментариев 1 или 2 или 3

    # 7. Использование набора запросов для динамической оценки списка значений вместо предоставления списка литеральных значений:
    inner_qs = Blog.objects.filter(name__contains='Путешествия')
    entries = Entry.objects.filter(blog__in=inner_qs)
    print("7 ", entries)

    # 8. Больше чем; Больше равно чем; Меньше чем; Меньше равно чем (gt, gte, lt, lte)
    # Вывести все записи, у которых число комментарием больше 10
    print("8 ", Entry.objects.filter(number_of_comments__gt=10))
    # Вывести все записи, которые опубликованы (поле pub_date) позже и равное 01.06.2023
    import datetime

    print("8 ", Entry.objects.filter(pub_date__gte=datetime.date(2023, 6, 1)))

    # Вывести все записи, у которых число комментарием больше 10 и рейтинг < 4
    print("8 ", Entry.objects.filter(number_of_comments__gt=10).filter(rating__lt=4))

    # Вывести все записи, у которых заголовок статьи лексиграфически <= "Зя"
    print("8 ", Entry.objects.filter(headline__lte="Гя"))

    # 9. Начинается с (с/без учетом регистра), заканчивается на (с/без учетом регистра) (startswith, istartswith, endswith, iendswith)
    print("9 ", Entry.objects.filter(headline__startswith='Как'))
    print("9 ", Entry.objects.filter(headline__endswith='ния'))

    # 10. Диапазон проверки (включительно) (range)
    # Вывести записи между 01.01.2023 и 31.12.2023
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    print("10 ", Entry.objects.filter(pub_date__range=(start_date, end_date)))

    # При данной постановке задачи (вывод за конкретный год) будет проще воспользоваться __year результат будет аналогичен
    print("10 ", Entry.objects.filter(pub_date__year=2023))

    # 11. Для полей даты и даты и времени точное совпадение (year, month, day, week, week_day, quarter, hour, minute, second)
    # Вывести записи старше 2022 года
    print("11 ", Entry.objects.filter(pub_date__year__lt=2022))
    # Вывести все записи за февраль доступных годов, отобразить название, дату публикации, заголовок
    print("11 ", Entry.objects.filter(pub_date__month=2).values('blog__name', 'pub_date', 'headline'))
    # Вывести username авторов у которых есть публикации с 1 по 15 апреля 2023 года, вывести без использования range. Пример для работы с __day
    # Сначала отфильтровываем по году, затем по дням, затем получаем значения имен у авторов и говорим, чтобы не было повторов
    print("11 ", Entry.objects.filter(pub_date__year=2023).filter(pub_date__month=4).filter(pub_date__day__gte=1).filter(
        pub_date__day__lte=15).values_list("author__name").distinct())
    # Вывести статьи опубликованные в понедельник (так как datetime работает по американской системе,
    # то начало недели идёт с воскресенья, а заканчивается субботой, поэтому понедельник второй день в неделе)
    print(Entry.objects.filter(pub_date__week_day=2).values('blog__name', 'pub_date', 'headline'))

    # 12. Для полей даты и времени преобразует значение как дату или время. (date, time)
    # Нужно быть внимательным так как __date и __time не применить к полям типа DateField, только к DateTimeField
    # Вывод всех записей по конкретной дате
    print("12 ", Entry.objects.filter(pub_date__date=datetime.date(2021, 6, 1)))
    # Вывод всех записей новее конкретной даты
    print("12 ", Entry.objects.filter(pub_date__date__gt=datetime.date(2024, 1, 1)))
    # Вывод записей по конкретному времени
    print(Entry.objects.filter(pub_date__time=datetime.time(12, 00)))
    # Вывод записей по временному диапазону с 6 утра до 17 вечера
    print(Entry.objects.filter(pub_date__time__range=(datetime.time(6), datetime.time(17))))

    # 13. Принимает True или False, которые соответствуют SQL-запросам IS NULL и IS NOT NULL, соответственно (isnull)
    # Вывести всех авторов которые не указали город
    print("13 ", AuthorProfile.objects.filter(city__isnull=True))

    # 14. Чувствительное/нечувствительное к регистру совпадение регулярного выражения.(regex, iregex)
    # Вывести записи где в тексте статьи встречается патерн \w*стран\w*
    print("14 ", Entry.objects.filter(body_text__regex=r'\w*стран\w*'))
    # Вывести записи авторов с почтовыми доменами @gmail.com и @mail.ru
    print("14 ", Entry.objects.filter(author__email__iregex=r'\w+(@gmail.com|@mail.ru)'))
    # Если необходимо вывести записи авторов с почтовыми доменами @gmail.com и @mail.ru, но чтобы значения не повторялись, то используем distinct()
    print("14 ", Entry.objects.filter(author__email__iregex=r'\w+(@gmail.com|@mail.ru)').distinct())

    # Применяемые методы для формирования запроса #

    # 15. Вывод всех значений в таблице objects.all()
    all_obj = Blog.objects.all()
    print("15 ", "Вывод всех значений в таблице Blog\n", all_obj)

    # 16. Вывод первого значения objects.first()
    all_obj = Blog.objects.first()
    print("16 ", "Вывод первого значения в таблице Blog\n", all_obj)

    # Последовательность запросов #

    # 17. Также можно вывести так, так как QuerySet не выполяются сразу и можно делать разные запросы последовательно сужая область, при этом запросы останутся. QuerySet выполнится при обращении к нему: list, for, print, получение объекта по индексу и т.д
    all_obj = Blog.objects.all()
    obj_first = all_obj.first()
    print("17 ", "Разные запросы на вывод в Blog\n", f"Первое значение таблицы = {obj_first}\n",
          f"Все значения = {all_obj}")

    # Итерируемость #

    # 18. Объект QuerySet итерируемый, а значит есть возможность обращения через [] и слайсирование, for и т.д
    all_obj = Blog.objects.all()
    for idx, value in enumerate(all_obj):
        print("18 ", f"idx = {idx}, value = {value}")
    print("18 ", all_obj[0])  # Получение 0-го элемента
    print("18 ", all_obj[2:4])  # Получение 2 и 3 элемента
    """Получение последнего элемента не осуществимо через обратный индекс
    all_obj[-1] - нельзя
    можно воспользоваться latest('<name_field>'), где <name_field> - имя колонки в БД.

    Почти все операции над БД не требуют предварительного получения всех элементов, постоянная запись Blog.objects.all()
    просто для примера.
    """
    print("18 ", all_obj.latest("id"))  # Получение последнего элемента
    print("18 ", Blog.objects.latest("id"))  # Одинаково работает

    # 19. Для получения конкретного элемента необходимо использовать objects.get(**conditions), где **conditions - условия их может быть не одно
    # Пример получения элемента по одному условию
    print("19 ", Blog.objects.get(id=1))
    # Пример получения элемента по двум условиям. Условия работают с оператором И, т.е. выведется строка, только с
    # совпадением и первого и второго параметра.
    print("19 ", Blog.objects.get(id=1, name="Путешествия по миру"))
    # Если нет совпадений, то выйдет исключение "db.models.Blog.DoesNotExist: Blog matching query does not exist."
    #print("19 ", Blog.objects.get(id=2, name="Путешествия по миру"))

    # 20. Когда необходимо вывести более одного значения то можно использовать objects.filter(**conditions), **conditions аналогично get(**conditions)
    print("20 ", Blog.objects.filter(id__gte=2))  # Вывод всех строк таблицы Blog у которых значение id >= 2.
    # Рассмотрение поиска по полям далее

    # 21. Аналогично фильтру, только противоположность. exclude() Возвращает новый QuerySet, содержащий объекты, которые не соответствуют указанным параметрам поиска.
    print("21 ", Blog.objects.exclude(id__gte=2))  # Вывод всех строк таблицы Blog кроме тех у которых значение id >= 2.

    # 22. Для проверки существования элемента(ов) в БД есть exists(), правда он применяется прямо к объекту, но только к объекту
    # objects.filter(**conditions).exists()
    # Для get придётся использовать блок try-except и ловить исключение MyModel.DoesNotExist, где MyModel ваша модель
    # Пример для get
    try:
        Blog.objects.get(id=2, name="Путешествия по миру")
    except Blog.DoesNotExist:
        print("22 ", "Не существует")
    # Пример для filter
    print("22 ", Blog.objects.filter(id=2, name="Путешествия по миру").exists())

    # 23. Чтобы подсчитать количество записей в запросе существует метод count() который применяют к объекту запроса
    print("23 ", Blog.objects.count())  # Можно ко всей таблице
    print("23 ", Blog.objects.filter(id__gte=2).count())  # Можно к запросу
    all_data = Blog.objects.all()
    filtred_data = all_data.filter(id__gte=2)
    print("23 ", filtred_data.count())  # Можно к частным запросам

    # 24. По умолчанию результаты, возвращаемые QuerySet, упорядочиваются с помощью кортежа, заданного параметром ordering в классе Meta модели.
    # Вы можете переопределить это для каждого QuerySet, используя метод order_by
    filtered_data = Blog.objects.filter(id__gte=2)
    print("24 ", filtered_data.order_by("id"))  # упорядочивание по возрастанию по полю id
    print("24 ", filtered_data.order_by("-id"))  # упорядочивание по уменьшению по полю id
    print("24 ", filtered_data.order_by("-name", "id"))  # упорядочивание по двум параметрам, сначала по первому на уменьшение,
    # затем второе на увеличение. Можно упорядочивание провести по сколь угодно параметрам.

    # 25. Аннотирует каждый объект в QuerySet с помощью предоставленного списка выражений запроса. Выражение может быть простым значением,
    # ссылкой на поле в модели (или любых связанных моделях) или агрегированным выражением (средние значения, суммы и т.д.),
    # которое было вычислено для объектов, связанных с объектами в QuerySet.
    from django.db.models import Count

    # Запрос, аннотирующий количество статей для каждого блога,
    # при этом добавляется новая колонка number_of_entries для вывода
    entry = Blog.objects.annotate(number_of_entries=Count('entries')).values('name', 'number_of_entries')
    print("25 ", entry)

    # 26. alias() То же, что annotate(), но вместо аннотирования объектов в QuerySet сохраняет выражение для последующего повторного
    # использования с другими методами QuerySet. Это полезно, когда результат самого выражения не нужен, но он используется
    # для фильтрации, упорядочивания или как часть сложного выражения. Таким образом, основная разница между
    # annotate() и alias() заключается в том, что annotate() используется для добавления агрегированных значений к каждому
    # объекту в QuerySet, тогда как alias() используется для создания псевдонимов для полей или связей в запросе, чтобы
    # использовать их в других частях запроса
    blogs = Blog.objects.alias(number_of_entries=Count('entries')).filter(number_of_entries__gt=4)
    print("26 ", blogs)

    # 27. Аргумент aggregate() описывает агрегированное значение, которое мы хотим вычислить aggregate() - это терминальное
    # предложение для QuerySet, которое при вызове возвращает словарь пар имя-значение. Имя - это идентификатор совокупного
    # значения; значение - это вычисленный агрегат. Имя автоматически генерируется из имени поля и агрегатной функции.
    # Всего поддерживаются данные агрегационные функции:
    #
    # Avg
    # Count
    # Max, Min
    # StdDev, Variance
    # Sum
    from django.db.models import Avg, Q

    # AVG
    # class Avg(expression, output_field=None, distinct=False, filter=None, default=None, **extra)
    # Вычислить среднюю оценку только для уникальных значений
    average_rating = Entry.objects.aggregate(
        average_rating1=Avg('rating', distinct=True)
    )
    print("27 ", average_rating)  # {'average_rating1': 3.6999999999999993}

    # Вычислить среднюю оценку с заданным значением по умолчанию(допустим
    # значение у поля None), если агрегация не возвращает результат
    average_rating_with_default = Entry.objects.aggregate(
        average_rating2=Avg('rating', default=5.0)
    )
    print("27 ", average_rating_with_default)  # {'average_rating2': 3.46}

    # Вычислить среднюю оценку только для статей, опубликованных после 2023 года
    average_rating = Entry.objects.aggregate(
        average_rating3=Avg('rating', filter=Q(pub_date__year__gt=2023)))
    print("27 ", average_rating)  # {'average_rating3': 2.925}

    # 28. Count
    # Возвращает количество объектов, связанных через предоставленное выражение.
    # class Count(expression, distinct=False, filter=None, **extra)
    from django.db.models import Count

    # Вычислить число уникальных авторов статей(которые написали хотя бы одну статью)
    count_authors = Entry.objects.aggregate(
        count_authors=Count('author', distinct=True)
    )
    print("28 ", count_authors)  # {'count_authors': 12}

    # Получить статьи с количеством тегов
    entries_with_tags_count = Entry.objects.annotate(
        tag_count=Count('tags')).values('id', 'tag_count')
    print("28 ", entries_with_tags_count)

    # 29. Max, Min
    # Возвращает максимальное/минимальное значение данного выражения
    # class Max(expression, output_field=None, filter=None, default=None, **extra)
    # class Min(expression, output_field=None, filter=None, default=None, **extra)
    from django.db.models import Max, Min

    # Вычислить максимальную и минимальную оценку
    calc_rating = Entry.objects.aggregate(
        max_rating=Max('rating'), min_rating=Min('rating')
    )
    print("29 ", calc_rating)  # {'max_rating': 5.0, 'min_rating': 0.0}

    # 30. StdDev, Variance
    # Возвращает стандартное отклонение данных в предоставленном выражении.
    # Возвращает дисперсию данных в предоставленном выражении
    # class StdDev(expression, output_field=None, sample=False, filter=None, default=None, **extra)
    # class Variance(expression, output_field=None, sample=False, filter=None, default=None, **extra)
    from django.db.models import StdDev, Variance

    # Вычислить среднее квадратическое отклонение и дисперсию оценки
    calc_rating = Entry.objects.aggregate(
        std_rating=StdDev('rating'), var_rating=Variance('rating')
    )
    print("30 ", calc_rating)  # {'std_rating': 1.6577092628081682, 'var_rating': 2.748}

    # 31. Sum
    # Вычисляет сумму всех значений данного выражения
    # class Sum(expression, output_field=None, distinct=False, filter=None, default=None, **extra)
    from django.db.models import Sum

    # Вычислить общее число комментариев в БД
    calc_rating = Entry.objects.aggregate(
        sum_comments=Sum('number_of_comments')
    )
    print("31 ", calc_rating)  # {'sum_comments': 134}

    # 32. reverse()
    # Изменение порядка вывода элемента из QuerySet. Похоже по действию на order_by.
    # Применяется когда известен порядок, чтобы потом его поменять.
    filtered_data = Blog.objects.filter(id__gte=2).order_by("id")
    print("32 ", filtered_data)  # упорядочивание по возрастанию по полю id
    print("32 ", filtered_data.reverse())  # поменяли направление

    # 33. distinct()
    # Возвращает новый QuerySet, который использует SELECT DISTINCT в своем SQL-запросе.
    # Это исключает повторяющиеся строки из результатов запроса.
    #print("33 ", Entry.objects.order_by('author', 'pub_date').distinct('author', 'pub_date'))  # Не работает в SQLite
    # distinct('author', 'pub_date') - оставляет уникальные строки по колонкам author, pub_date
    # distinct() - старается оставить уникальные данные по всем колонкам
    # Аналогично с поиском по полю можно обращаться к связанным данным distinct('author__name', 'pub_date')

    # 34. values()
    # Возвращает QuerySet, который возвращает словари, а не экземпляры модели, когда используется как итеративный.
    # Каждый из этих словарей представляет объект с ключами, соответствующими именам атрибутов объектов модели.
    # Обычный запрос
    print("34 ", Blog.objects.filter(name__startswith='Фитнес'))
    # Запрос раскрывающий значения
    print("34 ", Blog.objects.filter(name__startswith='Фитнес').values())
    # Вывод всех строк с их раскрытием
    print("34 ", Blog.objects.values())
    # Вывод всех строк с сохранением в запросе только необходимых столбцов
    print("34 ", Blog.objects.values('id', 'name'))  # Обратите внимание, что данные отсортированы по полю name

    # 35. values_list()
    # Это похоже на values(), за исключением того, что вместо возврата словарей он возвращает кортежи при повторении.
    # Каждый кортеж содержит значение из соответствующего поля или выражения,
    # переданное в вызов values_list() - поэтому первый элемент является первым полем и т.д.
    # Вывод всех строк с их раскрытием
    print("35 ", Blog.objects.values_list())
    # Вывод всех строк с сохранением в запросе только необходимых столбцов
    print("35 ", Blog.objects.values_list('id', 'name'))  # Обратите внимание, что данные отсортированы по полю name

    # 36. union()
    # union() использует оператор SQL UNION для объединения результатов двух или более QuerySet’ов
    # Применение оператора union() к нескольким QuerySets в данном формате позволяет выполнять операцию объединения в цепочке,
    # добавляя все нужные QuerySets в порядке их объединения
    # qs1.union(qs2, qs3)
    # или так
    # qs1.union(qs2).union(qs3)
    """
    Допустим, у нас есть три конкретных блога. Мы хотим получить объединение записей из этих трех блогов в один QuerySet.
    """
    blog_a_entries = Entry.objects.filter(blog__name='Путешествия по миру')
    blog_b_entries = Entry.objects.filter(blog__name='Кулинарные искушения')
    blog_c_entries = Entry.objects.filter(blog__name='Фитнес и здоровый образ жизни')
    result_qs = blog_a_entries.union(blog_b_entries, blog_c_entries)
    print("36 ", result_qs)
    # Для такой задачи может хорошо подойти in (ответ будет аналогичен), правда порядок может быть другой
    print("36 ", Entry.objects.filter(blog__name__in=[
                                        'Путешествия по миру',
                                        'Кулинарные искушения',
                                        'Фитнес и здоровый образ жизни'
                                        ]))

    # 37. intersection()
    # intersection() использует оператор SQL INTERSECT для возврата общих элементов двух или более QuerySet’ов.
    # Применение оператора intersection() к нескольким QuerySets позволяет найти пересечение записей между ними.
    # qs1.intersection(qs2, qs3)
    # qs1.intersection(qs2).intersection(qs3)
    """
    Допустим, у нас есть три конкретных блога. Мы хотим получить авторов, которые написали статью во всех из перечисленных блогах.
    """
    blog_a_entries = Entry.objects.filter(blog__name='Путешествия по миру').values('author')
    blog_b_entries = Entry.objects.filter(blog__name='Кулинарные искушения').values('author')
    blog_c_entries = Entry.objects.filter(blog__name='Фитнес и здоровый образ жизни').values('author')
    result_qs = blog_a_entries.intersection(blog_b_entries, blog_c_entries)
    print("37 ", result_qs)
    # <QuerySet [{'author': 1}, {'author': 9}, {'author': 20}]>

    # 38. difference()
    # difference() использует оператор SQL EXCEPT для хранения только элементов, присутствующих в QuerySet,
    # но не в каких-либо других QuerySet’ах.
    # qs1.difference(qs2, qs3)
    # qs1.difference(qs2).difference(qs3)
    """
    Вывести авторов, которые не написали ни одной статьи, в приведенных блогах
    """
    blog_a_entries = Entry.objects.filter(blog__name='Путешествия по миру').values('author')
    blog_b_entries = Entry.objects.filter(blog__name='Кулинарные искушения').values('author')
    blog_c_entries = Entry.objects.filter(blog__name='Фитнес и здоровый образ жизни').values('author')
    result_qs = Entry.objects.values('author').difference(blog_a_entries, blog_b_entries, blog_c_entries)
    print("38 ", result_qs)
    # <QuerySet [{'author': 5}, {'author': 7}, {'author': 8}]>

    # А допустим так (один из возможных запросов) можно узнать кто вообще не написал ни одной статьи в любой блог,
    # так как нет записей у этого автора в таблице Entry в поле author
    print("38 ", Author.objects.filter(entries__author=None).values('id'))

    # 39. select_related()
    # Возвращает QuerySet, который будет «следовать» отношениям внешнего ключа, выбирая дополнительные данные
    # связанного объекта при выполнении своего запроса. Это повышение производительности, которое приводит
    # к одному более сложному запросу, но означает, что дальнейшее использование отношений внешнего ключа
    # не потребует запросов к базе данных.
    # Следующие примеры иллюстрируют разницу между простыми поисками и с использованием select_related().
    # Для отображаения характеристик запросов воспользуемся connection из django.db. connection.queries позволяют
    # получить словарь, где содержится запрос в БД и время его выполнения
    # Также можно использовать django-debug-toolbar или django-silk

    # Стандартный поиск:
    from django.db import connection

    print("39 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  0  Запросы =  []
    """
    entry = Entry.objects.get(id=5)
    print("39 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  1  Запросы =  [...]
    """
    blog = entry.blog
    print("39 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  2  Запросы =  [...,...]
    """
    print("39 ", 'Результат запроса = ', blog)
    """
    Результат запроса =  Путешествия по миру
    """

    # Пример с select_related
    from django.db import connection

    print("39 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  0  Запросы =  []
    """
    entry = Entry.objects.select_related('blog').get(id=5)
    print("39 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  1  Запросы =  [...]
    """
    blog = entry.blog
    print("39 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  1  Запросы =  [...,...]
    """
    print("39 ", 'Результат запроса = ', blog)
    """
    Результат запроса =  Путешествия по миру
        """
    # Вы можете ссылаться на любое отношение ForeignKey или OneToOneField в списке полей, передаваемых в select_related()
    # Как видно, select_related() позволил уменьшить число запросов, так как при первом запросе подтянул данные
    # из связанных полей. Если в select_related ничего не передать, то будут загружены все отношения, однако только
    # для первого уровня вложенности.
    # В Django вы можете прописать select_related для отношений более чем двух уровней вложенности, используя точечную нотацию.

    # 40. prefetch_related()
    # Возвращает QuerySet, который автоматически извлекает в одном пакете связанные объекты для каждого из указанных поисков.
    # prefetch_related имеет цель, аналогичную select_related, в том смысле, что оба предназначены для урезания
    # количества запросов к базе данных, вызванного доступом к связанным объектам, но стратегия совершенно иная.
    # Стандартный
    from django.db import connection

    print("40 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  0  Запросы =  []
    """
    entry = Entry.objects.all()
    print("40 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  0  Запросы =  [], ввиду ленивости QuerySet
    """
    for row in entry:
        tags = [tag.name for tag in row.tags.all()]
        print("40 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
        print("40 ", 'Результат запроса = ', tags)
    """
    Число запросов =  26 Запросы = [...]
    """
    # с prefetch_related:
    from django.db import connection

    print("40.1 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  0  Запросы =  []
    """
    entry = Entry.objects.prefetch_related("tags")
    print("40.1 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    """
    Число запросов =  0  Запросы =  [], ввиду ленивости QuerySet
    """
    for row in entry:
        tags = [tag.name for tag in row.tags.all()]
        print("40.1 ", "Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
        print("40.1 ", 'Результат запроса = ', tags)
    """
    Число запросов =  2 Запросы = [...]
    """
    # В этом примере мы используем prefetch_related('tags'), чтобы загрузить все связанные авторы для каждой записи
    # блога Entry заранее. Затем мы можем получить доступ к связанным авторам для каждой записи блога, используя
    # атрибут tags, как обычно.
    # Важно отметить, что prefetch_related() выполняет дополнительный запрос к базе данных, чтобы предварительно
    # загрузить связанные объекты. Однако, это обычно более эффективный подход, особенно когда у вас есть множество
    # записей блога и связанных авторов, иначе каждая итерация по entry.tags.all() приведет к отдельному запросу
    # к базе данных для получения связанных авторов для каждой записи блога.
    # prefetch_related() позволяет сократить количество запросов и улучшить производительность при доступе к связанным объектам

    # Дополнительный функционал позволяющий создавать сложные запросы #

    # 41. F выражения
    # Объект F() представляет значение поля модели, преобразованное значение поля модели или
    # аннотированный столбец. Он позволяет ссылаться на значения полей модели и выполнять операции с базой данных,
    # используя их без необходимости извлекать их из базы данных в память Python
    from django.db.models import F

    """
    Вывести статьи где число комментариев на сайте больше числа комментариев на сторонних ресурсах
    """
    print("41 ", Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks')).values('id',
                                                                                       'number_of_comments',
                                                                                       'number_of_pingbacks'))
    """
    С аннотациями можно создать новый столбец с вычислением определенных характеристик
    """
    print("41 ", Entry.objects.annotate(sum_number=F('number_of_pingbacks') + F('number_of_comments')).values('id',
                                                                                                       'number_of_comments',
                                                                                                       'number_of_pingbacks',
                                                                                                       'sum_number'))
    """
    Или с alias для дальнейшего использования
    """
    print("41 ", Entry.objects.alias(sum_number=F('number_of_pingbacks') + F('number_of_comments')).
          annotate(val1=F('sum_number') / F('number_of_comments')).values('id',
                                                                          'number_of_comments',
                                                                          'number_of_pingbacks',
                                                                          'val1'))

    # 42. Q объекты
    # Объект Q() представляет собой условие SQL, которое может быть использовано в операциях, связанных с базой данных.
    # Это похоже на то, как объект F() представляет значение поля модели или аннотации. Они позволяют определять и
    # повторно использовать условия и объединять их с помощью таких операторов, как | (OR), & (AND) и ^ (XOR)
    from django.db.models import Q

    # Получение всех записей, у которых заголовок содержит 'ключевое слово' или текст содержит 'определенное слово'
    entries = Entry.objects.filter(
        Q(headline__icontains='тайны') | Q(body_text__icontains='город'))
    print("42 ", entries)

    # Получение записей блога "Путешествия по миру" с датами публикаций между 1 мая 2022 и 1 мая 2023
    from datetime import date

    entries = Entry.objects.filter(
        Q(blog__name='Путешествия по миру') & Q(pub_date__date__range=(date(2022, 5, 1), date(2023, 5, 1))))
    print("42 ", entries)

    # Получить статьи, у которых либо имеется оценка больше 4, либо число комментариев меньше 10 (используя XOR)
    entries = Entry.objects.filter(Q(rating__gt=4) ^ Q(number_of_comments__lt=10))
    print("43 ", entries)

    # 43. ExpressionWrapper()
    # ExpressionWrapper окружает другое выражение и предоставляет доступ к свойствам, таким как output_field,
    # которые могут быть недоступны для других выражений. ExpressionWrapper необходим при использовании арифметики
    # на выражениях F() с различными типами
    # class ExpressionWrapper(expression, output_field)

    # 44. Case, When, Value
    # Модуль Case позволяет создавать условные выражения в запросах, аналогично оператору CASE в SQL. Он может быть
    # использован для выполнения разных действий в зависимости от значений полей.
    # Модуль When в Django используется вместе с модулем Case для создания условных выражений в запросах. Он позволяет
    # определить условие и значение, которое должно быть возвращено, если условие выполняется.
    # Value - это выражение, которое позволяет явно указать значение для определенного поля или атрибута модели.
    # Оно полезно в тех случаях, когда вы хотите явно задать определенное значение в запросе или аннотации, вместо
    # получения его из базы данных или другого источника данных.

    # Получение всех записей с полем is_popular, которое равно True, если значение поля rating больше равно 4, иначе False
    from django.db.models import Case, When, BooleanField, CharField

    entries = Entry.objects.annotate(
        is_popular=Case(
            When(rating__gte=4, then=True),
            default=False,
            output_field=BooleanField()
        )
    ).values('id', 'rating', 'is_popular')
    print("44 ", entries)

    # Создание описательной метки для числа тегов в статье
    from django.db.models import Count, Value

    entries = Entry.objects.annotate(
        count_tags=Count("tags"),
        tag_label=Case(
            When(count_tags__gte=3, then=Value('Много')),
            When(count_tags=2, then=Value('Средне')),
            default=Value('Мало'),
            output_field=CharField()
        )
    ).values('id', 'count_tags', 'tag_label')
    print("44 ", entries)

    # 45. Subquery()
    # Вы можете добавить явный подзапрос к QuerySet с помощью выражения Subquery
    # class Subquery(queryset, output_field=None)
    # Subquery (подзапрос) в контексте базы данных и Django ORM представляет собой запрос, который выполняется внутри
    # другого запроса. Он используется для получения данных из одной таблицы или запроса и использования их в другом
    # запросе
    from django.db.models import Subquery

    # Получаем список ID авторов без биографии
    subquery = AuthorProfile.objects.filter(bio__isnull=True).values('author_id')

    # Фильтруем записи блога по авторам
    query = Entry.objects.filter(author__in=Subquery(subquery))
    print("45 ", query)

    # Аналогично можно подключиться так, так как есть непрямая связь между Author и AuthorProfile через первичный ключ
    print("45 ", Entry.objects.filter(author__authorprofile__bio__isnull=True))

    # 46. Необработанные выражения SQL
    # Иногда выражения базы данных не могут легко выразить сложное предложение WHERE.
    # В этих крайних случаях используйте выражение RawSQL
    from django.db import connection

    # Составляем SQL-запрос
    sql = """
    SELECT id, headline
    FROM db_train_alternative_entry
    WHERE headline LIKE '%%тайны%%' OR body_text LIKE '%%город%%'
    """
    # Выполняем запрос
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    # Выводим результаты
    for result in results:
        print("46 ", result)

    # Также можно вызвать метод raw() и передать туда параметры
    # Выполняем сырой SQL-запрос
    results = Entry.objects.raw(
        """
        SELECT id, headline
        FROM db_train_alternative_entry
        WHERE headline LIKE '%%тайны%%' OR body_text LIKE '%%город%%'
        """
    )
    # Выводим результаты
    for result in results:
        print("46 ", result.id, result.headline)

    # 47. Оконные функции
    # Оконные функции обеспечивают возможность применения функций на разделах. В отличие от обычной агрегатной функции,
    # которая вычисляет конечный результат для каждого набора, определенного группой, оконные функции работают над
    # frames и разделами и вычисляют результат для каждой строки.
    # class Window(expression, partition_by=None, order_by=None, frame=None, output_field=None)
    from django.db.models import F, Window, Avg, Max, Min

    # Получаем queryset статей блога с аннотациями, используя оконные функции
    queryset = Entry.objects.annotate(
        avg_comments=Window(
            expression=Avg('number_of_comments'),
            partition_by=F('blog'),
        ),
        max_comments=Window(
            expression=Max('number_of_comments'),
            partition_by=F('blog'),
        ),
        min_comments=Window(
            expression=Min('number_of_comments'),
            partition_by=F('blog'),
        ),

    ).values('id', 'headline', 'avg_comments', 'max_comments', 'min_comments')
    print(queryset)


























