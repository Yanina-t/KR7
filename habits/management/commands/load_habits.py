import json
from django.core.management.base import BaseCommand
from habits.models import Habit


class Command(BaseCommand):
    help = 'Load habits from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        with open(filename, 'r') as f:
            habits_data = json.load(f)
            for habit_data in habits_data:
                Habit.objects.create(**habit_data)
        self.stdout.write(self.style.SUCCESS('Habits have been successfully loaded from JSON file.'))
