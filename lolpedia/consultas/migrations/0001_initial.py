# Generated by Django 3.0.5 on 2021-05-20 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.Season')),
            ],
        ),
        migrations.CreateModel(
            name='Split',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.League')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('split', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.Split')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=280)),
                ('team', models.CharField(max_length=280)),
                ('wins', models.IntegerField()),
                ('loses', models.IntegerField()),
                ('split', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.Split')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home', models.CharField(max_length=280)),
                ('visitor', models.CharField(max_length=280)),
                ('result', models.CharField(max_length=280)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.Round')),
            ],
        ),
    ]
