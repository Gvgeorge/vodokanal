# Generated by Django 4.0.4 on 2022-05-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdkapp', '0004_rates'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='message_sent',
            field=models.BooleanField(default=False),
        ),
    ]
