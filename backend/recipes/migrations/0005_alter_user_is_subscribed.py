# Generated by Django 3.2.3 on 2024-10-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
