# Generated by Django 5.1.1 on 2024-10-18 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='friends',
        ),
    ]
