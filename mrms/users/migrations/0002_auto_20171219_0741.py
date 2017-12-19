# Generated by Django 2.0 on 2017-12-19 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mrms', '__first__'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateMedicalCouncil',
            fields=[
                ('datetimemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='mrms.DateTimeModel')),
                ('state_medical_council_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Enter medical code as per : https://www.mciindia.org/ActivitiWebClient/informationdesk/indianMedicalRegister')),
                ('state_medical_council_name', models.CharField(max_length=150)),
            ],
            bases=('mrms.datetimemodel',),
        ),
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateField(default='1987-09-13'),
        ),
        migrations.AddField(
            model_name='user',
            name='doctor_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='doctor_date_of_reg',
            field=models.DateField(default=None, null=True, verbose_name='Date of Registration'),
        ),
        migrations.AddField(
            model_name='user',
            name='doctor_registration_number',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='Medical Council Registration Number'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='undisclosed', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='doctor_state_medical_council',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.StateMedicalCouncil', verbose_name='Medical Council'),
        ),
    ]
