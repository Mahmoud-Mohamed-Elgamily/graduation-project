# Generated by Django 2.1 on 2019-06-09 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20190328_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdata',
            name='identityNumber',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='studentdata',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile'),
        ),
        migrations.AlterField(
            model_name='studentdata',
            name='studentPhoneNumber',
            field=models.CharField(max_length=15),
        ),
    ]