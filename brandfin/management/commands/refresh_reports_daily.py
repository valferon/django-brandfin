from django.core.management.base import BaseCommand, CommandError
import datetime

from brandfin.models import Query


class Command(BaseCommand):
    help = 'Refresh the active database schema'

    def handle(self, *args, **options):

        """
        Update the scheduled reports
        :param args:
        :param options:
        """

        self.stdout.write('Starting refres reports task')
        today = datetime.date.today().strftime('%Y-%m-%d')
        scheduled_reports = Query.objects.filter(daily_run=True)

        for report in scheduled_reports:
            report.pk = None

            report.title = report.title+' - Run date : '+today
            report.result_headers = None
            report.result_data = None
            report.daily_run = False
            report.execute()
            report.save()
            self.stdout.write('Successfully refreshed report "%s"' %report.title )
