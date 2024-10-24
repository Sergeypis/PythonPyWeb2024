# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# alter DevDB2024 set search_path to "Cars", "Clients", "Operations", public;
# alter role postgres set search_path to "Cars", "Clients", "Operations", public;
from django.db import models


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
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


class Passenger(models.Model):
    pass_id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    passport = models.CharField(max_length=12)
    birthday = models.DateField()

    class Meta:
        managed = True
        db_table = 'Passenger'
        unique_together = (('lastname', 'firstname', 'passport', 'birthday'),)


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    depart = models.CharField(max_length=30)
    arrive = models.CharField(max_length=30)
    distance = models.IntegerField()
    trip_time = models.CharField(max_length=30)
    active = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Route'
        unique_together = (('depart', 'arrive', 'distance'),)


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, models.DO_NOTHING)
    vin = models.CharField(max_length=17)
    date_depart = models.DateField()
    time_depart = models.TimeField()
    driver = models.ForeignKey(Driver, models.DO_NOTHING, blank=True, null=True)
    tickets_avaliable = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Schedule'
        unique_together = (('vin', 'date_depart', 'time_depart'),)


class Ticket(models.Model):
    ticked_id = models.AutoField(primary_key=True)
    schedule_id = models.IntegerField()
    pass_field = models.ForeignKey(Passenger, models.DO_NOTHING, db_column='pass_id')  # Field renamed because it was a Python reserved word.
    cost = models.TextField()  # This field type is a guess.
    place_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Ticket'
        unique_together = (('schedule_id', 'pass_field'), ('schedule_id', 'place_number'),)


class Vehicle(models.Model):
    vin = models.CharField(primary_key=True, max_length=17)
    model = models.CharField(max_length=30)
    number_plate = models.CharField(max_length=12)
    year_of_manufacture = models.IntegerField()
    number_of_seats = models.IntegerField()
    type = models.ForeignKey('VehicleType', models.DO_NOTHING, db_column='type', blank=True, null=True)
    fuel_type = models.CharField(max_length=30, blank=True, null=True)
    resource = models.IntegerField()
    mileage = models.IntegerField()
    decommissioned = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Vehicle'
        unique_together = (('model', 'number_plate', 'year_of_manufacture'),)


class VehicleType(models.Model):
    type = models.CharField(primary_key=True, max_length=30)
    max_allowed_speed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Vehicle_type'
