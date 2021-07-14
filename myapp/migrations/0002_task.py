# Generated by Django 3.2.5 on 2021-07-14 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('status', models.BooleanField(default='incomplete')),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasktouser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
