from django.core.management.base import BaseCommand, CommandError
import datetime

from models import Query


class Command(BaseCommand):
    help = 'Refresh the active database schema'

    def handle(self, *args, **options):

        """
        Update the scheduled reports
        :param args:
        :param options:
        """
        scheduled_reports = Query.objects.filter(daily_run=True)

        for report in scheduled_reports:
            report.pk = None
            report.title = report.title+' '+datetime.date.today()
            report.result_headers = None
            report.execute()
            report.save()
            self.stdout.write('Successfully refreshed report "%s"' %report.title )