# Generated by Django 4.2.6 on 2023-11-29 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solidify', '0006_rename_nr_voluntario_evento_nr_voluntarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voluntarios_evento',
            name='NOME',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
