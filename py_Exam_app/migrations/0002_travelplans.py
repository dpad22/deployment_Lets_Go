# Generated by Django 2.2.4 on 2020-04-26 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('py_Exam_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Travelplans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('travel_start', models.DateTimeField()),
                ('travel_end', models.DateTimeField()),
                ('favorite', models.ManyToManyField(related_name='favorite', to='py_Exam_app.User')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_by', to='py_Exam_app.User')),
            ],
        ),
    ]
