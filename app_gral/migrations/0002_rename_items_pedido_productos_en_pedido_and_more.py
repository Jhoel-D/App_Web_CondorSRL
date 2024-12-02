# Generated by Django 5.1.3 on 2024-11-27 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_gral', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='items',
            new_name='productos_en_pedido',
        ),
        migrations.RenameField(
            model_name='ventas',
            old_name='productos',
            new_name='productos_de_venta',
        ),
        migrations.AddField(
            model_name='usuario',
            name='imagen_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='bd_images/', verbose_name='Image'),
        ),
    ]
