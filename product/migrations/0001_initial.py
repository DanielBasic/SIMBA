# Generated by Django 4.2.2 on 2023-09-03 01:45

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('price', models.FloatField(null=True)),
                ('seller', models.IntegerField(null=True)),
                ('tracking_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_tracking_activated', models.BooleanField(default=True)),
                ('group', models.ManyToManyField(to='groupings.group_by_ad')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
