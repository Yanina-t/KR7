# Generated by Django 5.0.3 on 2024-03-13 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_remove_habit_user_habit_owner_habit_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='title',
            field=models.CharField(max_length=100, verbose_name='название привычки'),
        ),
    ]