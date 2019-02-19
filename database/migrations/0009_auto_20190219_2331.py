# Generated by Django 2.1.2 on 2019-02-19 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20190215_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdata',
            name='address',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='age',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='birthDate',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='gender',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='grades',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='homeNumber',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='identityNumber',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='instituteName',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='instituteYear',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='nationality',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='parentName',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='parentPhoneNumber',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='qualification',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='schoolYear',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='seatNumber',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='studentPhoneNumber',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='turn',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
