# Generated by Django 3.2.13 on 2022-07-03 03:34

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eval_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Available',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areas', models.CharField(blank=True, max_length=200, null=True)),
                ('pokemons', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('location', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='eval_test.locations')),
            ],
        ),
    ]
