from django.core.management.base import BaseCommand, CommandError
from sqlalchemy import inspect
import json

from brandfin.models import Schema, DataConnection
from utils import _format_sqlalch_field


class Command(BaseCommand):
    help = 'Refresh the active database schema'

    def handle(self, *args, **options):

        """
        Update the active database schema
        :param args:
        :param options:
        """
        schema_list = []
        db_list = DataConnection.objects.all()

        for db in db_list:
            if DataConnection.get_db_active(db) == True:
                try:
                    schema = Schema.objects.get(source=db)
                    moteur = DataConnection.get_db_engine(db)
                    insp = inspect(moteur)
                    for table in insp.get_table_names():
                        columns = insp.get_columns(table)
                        schema_list.append((
                            table,
                            [_format_sqlalch_field(f) for f in columns]
                        ))

                    json_schema = json.dumps(schema_list)
                    schema.schemaData = json_schema
                    schema.save()
                except Schema.DoesNotExist:
                    raise CommandError('Schema for db "%s" does not exist' % db.name)

                self.stdout.write('Successfully updated schema for db "%s"' % db.name)
