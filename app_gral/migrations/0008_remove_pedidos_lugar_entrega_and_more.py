# Generated by Django 5.1.3 on 2024-12-09 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_gral', '0007_pedidos_monto_adelanto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidos',
            name='lugar_entrega',
        ),
        migrations.RemoveField(
            model_name='pedidos',
            name='monto_adelanto',
        ),
    ]