# Generated by Django 4.0.4 on 2022-05-23 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.IntegerField(primary_key=True, serialize=False)),
                ('row_nubmer', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
