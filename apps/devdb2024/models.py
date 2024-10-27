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
        validators=[regex_trip_time_field])
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Route'
        unique_together = (('depart', 'arrive', 'distance'),)


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


class VehicleType(models.Model):
    type = models.CharField(primary_key=True, max_length=30)
    max_allowed_speed = models.PositiveSmallIntegerField(null=True, default=70)

    class Meta:
        managed = True
        db_table = 'Vehicle_type'


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


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    route_id = models.ForeignKey(
        to=Route,
        on_delete=models.DO_NOTHING
    )
    vin = models.ForeignKey(
        to=Vehicle,
        on_delete=models.DO_NOTHING
    )
    date_depart = models.DateField()
    time_depart = models.TimeField()
    driver_id = models.ForeignKey(
        to=Driver,
        on_delete=models.SET_NULL,
        null=True)
    tickets_avaliable = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Schedule'
        unique_together = (('vin', 'date_depart', 'time_depart'),)


class Ticket(models.Model):
    ticked_id = models.AutoField(primary_key=True)
    schedule_id = models.ForeignKey(
        to=Schedule,
        on_delete=models.DO_NOTHING
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
