# Generated by Django 4.2.6 on 2023-12-02 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solidify', '0013_evento_ong_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='NR_OCUPADOS',
            field=models.IntegerField(null=True),
        ),
    ]
