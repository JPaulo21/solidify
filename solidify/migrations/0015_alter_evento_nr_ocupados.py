# Generated by Django 4.2.6 on 2023-12-02 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solidify', '0014_evento_nr_ocupados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='NR_OCUPADOS',
            field=models.IntegerField(default=0),
        ),
    ]
