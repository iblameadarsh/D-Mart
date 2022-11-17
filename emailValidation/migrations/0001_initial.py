# Generated by Django 3.2.15 on 2022-09-26 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailValidations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskName', models.TextField(blank=True, max_length=255, null=True)),
                ('rcpt_email', models.EmailField(blank=True, help_text='Email Field, max 255 characters.', max_length=254, null=True)),
                ('input_file', models.FileField(null=True, upload_to='files')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
