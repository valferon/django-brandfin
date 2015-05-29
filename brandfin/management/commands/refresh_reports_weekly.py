from django.core.management.base import BaseCommand, CommandError
import datetime

from brandfin.models import Query


class Command(BaseCommand):
    help = 'Refresh the weekly scheduled reports'

    def handle(self, *args, **options):

        """
        Update the scheduled reports
        :param args:
        :param options:
        """

        today = datetime.date.today().strftime('%Y-%m-%d')
        scheduled_reports = Query.objects.filter(weekly_run=True)

        for report in scheduled_reports:
            report.pk = None

            report.title = report.title+' - Weekly report : '+today
            report.result_headers = None
            report.result_data = None
            report.daily_run = False
            report.execute()
            report.save()
            self.stdout.write('Successfully refreshed report "%s"' %report.title )
