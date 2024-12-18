# Generated by Django 5.1.2 on 2024-11-01 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devdb2024', '0003_alter_test_options_test_at_create_alter_test_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTest',
            fields=[
                ('prkey', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('at_create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'db_table': 'TestTest',
                'managed': True,
            },
        ),
    ]
