# Generated by Django 2.0 on 2017-12-28 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phr', '0003_auto_20171228_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientevents',
            name='dcmimages',
            field=models.ManyToManyField(blank=True, null=True, to='phr.DCMImages'),
        ),
    ]
