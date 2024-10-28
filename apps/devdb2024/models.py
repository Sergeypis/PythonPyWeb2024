# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# alter DevDB2024 set search_path to "Cars", "Clients", "Operations", public;
# alter role postgres set search_path to "Cars", "Clients", "Operations", public;
# 'OPTIONS': {
#             'options': '-c search_path=<my>_schema'
from django.db import models
from django.core.validators import RegexValidator


class Route(models.Model):
    regex_trip_time_field = RegexValidator(
        regex=r'(?:\d\d?\s(?:days?)\s)?\b[0-2]?[0-9]:[0-5][0-9]\b',
        message=""
    )

    route_id = models.AutoField(primary_key=True)
    depart = models.CharField(max_length=30)
    arrive = models.CharField(max_length=30)
    distance = models.PositiveSmallIntegerField()
    trip_time = models.CharField(
        max_length=30,
        validators=[regex_trip_time_field]
    )
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Route'
        unique_together = (('depart', 'arrive', 'distance'),)
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return f"Маршрут: {self.depart} - {self.arrive}, {self.distance} км"


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, null=True)
    passport = models.CharField(max_length=12)
    birthday = models.DateField()
    date_of_employment = models.DateField()
    drivers_license = models.CharField(max_length=12)
    drivers_license_category = models.CharField(max_length=30)
    date_of_issue_license = models.DateField()

    class Meta:
        managed = True
        db_table = 'Driver'
        unique_together = (('lastname', 'firstname', 'passport', 'birthday'),)
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return f"Водитель: {self.firstname} {self.lastname}, категории ВУ - {self.drivers_license_category}"


class VehicleType(models.Model):
    type = models.CharField(primary_key=True, max_length=30)
    max_allowed_speed = models.PositiveSmallIntegerField(null=True, default=70)

    class Meta:
        managed = True
        db_table = 'Vehicle_type'
        verbose_name_plural = "Тип ТС"

    def __str__(self):
        return f"{self.type}"


class Vehicle(models.Model):
    vin = models.CharField(primary_key=True, max_length=17)
    model = models.CharField(max_length=30)
    number_plate = models.CharField(max_length=12)
    year_of_manufacture = models.IntegerField()
    number_of_seats = models.PositiveSmallIntegerField()
    type = models.ForeignKey(
        to=VehicleType,
        on_delete=models.SET_DEFAULT,
        default="not set",
        db_column='type',
        null=True
    )
    fuel_type = models.CharField(max_length=30, null=True)
    resource = models.IntegerField()
    mileage = models.PositiveSmallIntegerField()
    decommissioned = models.BooleanField(null=True, default=False)

    class Meta:
        managed = True
        db_table = 'Vehicle'
        unique_together = (('model', 'number_plate', 'year_of_manufacture'),)
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

    def __str__(self):
        return f"{self.model}, {self.number_plate}"


class Passenger(models.Model):
    pass_id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, null=True)
    passport = models.CharField(max_length=12)
    birthday = models.DateField()

    class Meta:
        managed = True
        db_table = 'Passenger'
        unique_together = (('lastname', 'firstname', 'passport', 'birthday'),)
        verbose_name = "Пассажир"
        verbose_name_plural = "Пассажиры"

    def __str__(self):
        initials = None  # Инициалы
        if self.firstname and self.patronymic:
            initials = f"{self.firstname.upper()[0]}.{self.patronymic.upper()[0]}."
        return f"{self.lastname} {initials}"


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    route_id = models.ForeignKey(
        to=Route,
        on_delete=models.DO_NOTHING,
        db_column="route_id"
    )
    vin = models.ForeignKey(
        to=Vehicle,
        on_delete=models.DO_NOTHING,
        db_column="vin"
    )
    date_depart = models.DateField()
    time_depart = models.TimeField()
    driver_id = models.ForeignKey(
        to=Driver,
        on_delete=models.SET_NULL,
        db_column="driver_id",
        null=True)
    tickets_avaliable = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Schedule'
        unique_together = (('vin', 'date_depart', 'time_depart'),)
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"

    def __str__(self):
        return f"Рейс {self.route_id.depart} - {self.route_id.arrive}, отправление {self.date_depart} {self.time_depart}"


class Ticket(models.Model):
    ticked_id = models.AutoField(primary_key=True)
    schedule_id = models.ForeignKey(
        to=Schedule,
        on_delete=models.DO_NOTHING,
        db_column="schedule_id"
    )
    pass_field = models.ForeignKey(
        to=Passenger,
        on_delete=models.DO_NOTHING,
        db_column='pass_id'  # Field renamed because it was a Python reserved word.
    )
    cost = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00
    )
    place_number = models.PositiveSmallIntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'Ticket'
        unique_together = (('schedule_id', 'pass_field'),)
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

    def __str__(self):
        return f"Билет {self.schedule_id.route_id.depart} - {self.schedule_id.route_id.arrive}, на {self.schedule_id.date_depart} место {self.place_number}"
