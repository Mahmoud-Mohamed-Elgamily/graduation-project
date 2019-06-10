# Generated by Django 2.1.2 on 2019-04-17 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '0009_auto_20190219_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.CharField(max_length=500, unique=True)),
                ('A', models.CharField(max_length=100)),
                ('B', models.CharField(max_length=100)),
                ('C', models.CharField(max_length=100)),
                ('D', models.CharField(max_length=100)),
                ('correct', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_enter', models.PositiveIntegerField(blank=True)),
                ('last_time', models.CharField(blank=True, max_length=50)),
                ('time', models.CharField(blank=True, max_length=50)),
                ('ip', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=500, unique=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('password', models.CharField(blank=True, max_length=10, unique=True)),
                ('Degree', models.PositiveIntegerField(blank=True)),
                ('finsh', models.BooleanField(blank=True)),
                ('questions', models.ManyToManyField(blank=True, related_name='AS', to='quizes.questions')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='DF474', to='database.Students_user')),
            ],
        ),
    ]