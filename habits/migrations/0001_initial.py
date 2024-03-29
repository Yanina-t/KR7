from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=100, verbose_name='Место')),
                ('time', models.TimeField(verbose_name='Время')),
                ('action', models.CharField(max_length=255, verbose_name='Действие')),
                ('is_rewardable', models.BooleanField(default=False, verbose_name='Вознаграждаемая привычка')),
                ('frequency', models.IntegerField(default=1, verbose_name='Периодичность (в днях)')),
                ('reward', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вознаграждение')),
                ('execution_time', models.IntegerField(verbose_name='Время выполнения (в секундах)')),
                ('is_public', models.BooleanField(default=False, verbose_name='Публичная привычка')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habits.habit', verbose_name='Связанная привычка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
            },
        ),
    ]
