# Generated by Django 4.2.6 on 2023-12-02 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solidify', '0011_alter_voluntarios_evento_cpf_voluntario'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='voluntarios_evento',
            unique_together={('ID_EVENTO', 'ID_VOLUNTARIO')},
        ),
    ]
