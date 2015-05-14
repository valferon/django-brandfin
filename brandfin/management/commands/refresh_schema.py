from django.core.management.base import BaseCommand, CommandError
from sqlalchemy import inspect
import json

from brandfin.models import Schema, DataConnection
from brandfin.utils import _format_sqlalch_field, get_dataconnection_active


class Command(BaseCommand):
    help = 'Refresh the active database schema'

    def handle(self, *args, **options):

        """
        Update the active database schema
        :param args:
        :param options:
        """
        schema_list = []

        db = get_dataconnection_active()
        if db != None:
            db_name = DataConnection.get_db_name(db)
            schema_name = "schema_" + db_name

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
                schema.schemaData = json.dumps(schema_list)
                schema.save()
                self.stdout.write('Successfully updated schema for db "%s"' % db.name)

            except Schema.DoesNotExist:
                moteur = DataConnection.get_db_engine(db)
                insp = inspect(moteur)
                for table in insp.get_table_names():
                    columns = insp.get_columns(table)
                    schema_list.append((
                        table,
                        [_format_sqlalch_field(f) for f in columns]
                    ))
                json_schema = json.dumps(schema_list)
                Schema.objects.create(schemaName=schema_name, source=db, schemaData=json_schema)
                self.stdout.write('Successfully created schema for db "%s"' % db.name)
