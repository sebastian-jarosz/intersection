# Generated by Django 3.1.5 on 2021-01-29 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_coordinate', models.FloatField()),
                ('y_coordinate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_1', to='segments.point')),
                ('point2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_2', to='segments.point')),
            ],
        ),
    ]
