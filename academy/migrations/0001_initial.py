# Generated by Django 4.2.2 on 2023-06-26 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('manager', models.CharField(max_length=75)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('liga', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('anio_nacimiento', models.PositiveIntegerField()),
                ('edad_descubrimiento', models.PositiveIntegerField()),
                ('media_descubrimiento', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=80)),
                ('bandera', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Posicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('POR', 'Portero'), ('LD', 'Lateral Derecho'), ('LI', 'Lateral Izquierdo'), ('DFC', 'Defensor Central'), ('MCD', 'Mediocampista Defensivo'), ('MC', 'Mediocampista Central'), ('MI', 'Mediocampista Izquierdo'), ('MD', 'Mediocampista Derecho'), ('MCO', 'Mediocampista Ofensivo'), ('SD', 'Segundo Delantero'), ('EI', 'Extremo Izquierdo'), ('ED', 'Extremo Derecho'), ('DC', 'Delantero Centro')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Temporada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='TemporadaJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.equipo')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.jugador')),
                ('temporada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.temporada')),
            ],
        ),
        migrations.CreateModel(
            name='TemporadaFinalizada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion_liga', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22')])),
                ('progreso_continental', models.CharField(choices=[('No clasificado', 'No clasificado'), ('Ronda 1', 'Ronda 1'), ('Ronda 2', 'Ronda 2'), ('Ronda 3', 'Ronda 3'), ('16º', '16º'), ('8º', '8º'), ('4º', '4º'), ('Semifinales', 'Semifinales'), ('Final', 'Final'), ('Campeon', 'Campeon')], max_length=255)),
                ('progreso_copa', models.CharField(choices=[('No clasificado', 'No clasificado'), ('Ronda 1', 'Ronda 1'), ('Ronda 2', 'Ronda 2'), ('Ronda 3', 'Ronda 3'), ('16º', '16º'), ('8º', '8º'), ('4º', '4º'), ('Semifinales', 'Semifinales'), ('Final', 'Final'), ('Campeon', 'Campeon')], max_length=255)),
                ('temporada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.temporada')),
            ],
        ),
        migrations.CreateModel(
            name='TemporadaEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.equipo')),
                ('temporada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.temporada')),
            ],
        ),
        migrations.AddField(
            model_name='jugador',
            name='nacionalidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.nacionalidad'),
        ),
        migrations.AddField(
            model_name='jugador',
            name='posiciones',
            field=models.ManyToManyField(related_name='jugador_posicion', to='academy.posicion'),
        ),
    ]