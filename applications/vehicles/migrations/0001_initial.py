# Generated by Django 4.1.2 on 2022-10-28 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=20, verbose_name='Nombre de la Marca')),
            ],
        ),
        migrations.CreateModel(
            name='TypeVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_vehicle', models.CharField(max_length=20, verbose_name='Tipo de vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.IntegerField(max_length=10, verbose_name='Modelo del Vehiculo')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_to_brand', to='vehicles.brand', verbose_name='Marca')),
                ('type_vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_to_type_vehicle', to='vehicles.typevehicle', verbose_name='Tipo Vehiculo')),
            ],
        ),
    ]
