import os
import csv
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps

class Command(BaseCommand):
    help = 'Backup database to .sql and .csv formats'

    def add_arguments(self, parser):
        parser.add_argument('--sql', type=str, help='File path for SQL backup')
        parser.add_argument('--csv', type=str, help='File path for CSV backup')
        parser.add_argument('--model', type=str, help='Model to backup in CSV format (app_label.model_name)')

    def handle(self, *args, **options):
        sql_path = options.get('sql')
        csv_path = options.get('csv')
        model_name = options.get('model')

        if sql_path:
            self.backup_to_sql(sql_path)
        if csv_path and model_name:
            self.backup_to_csv(model_name, csv_path)

    def backup_to_sql(self, file_path):
        with open(file_path, 'w') as f:
            call_command('dumpdata', format='sql', stdout=f)

    def backup_to_csv(self, model_name, file_path):
        model = apps.get_model(*model_name.split('.'))
        field_names = [field.name for field in model._meta.fields]

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)

            for instance in model.objects.all():
                writer.writerow([getattr(instance, field) for field in field_names])
