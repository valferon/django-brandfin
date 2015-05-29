from time import time
from datetime import datetime
import logging
import json

from django.db import models, DatabaseError
from django.core.urlresolvers import reverse
from django.conf import settings
import sqlalchemy
from sqlalchemy import exc

from utils import passes_blacklist, swap_params, extract_params, shared_dict_update, get_dataconnection_engine, AlchemyEncoder
import app_settings


MSG_FAILED_BLACKLIST = "Query failed the SQL blacklist."

logger = logging.getLogger(__name__)


class Query(models.Model):
    title = models.CharField(max_length=255)
    sql = models.TextField()
    description = models.TextField(null=True, blank=True)
    result_headers = models.TextField(null=True, blank=True)
    result_data = models.TextField(null=True, blank=True)
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run_date = models.DateTimeField(auto_now=True)
    daily_run = models.BooleanField(default=False, help_text="Schedule query to run daily")
    weekly_run = models.BooleanField(default=False, help_text="Schedule query to run weekly")

    def __unicode__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        self.params = kwargs.get('params')
        kwargs.pop('params', None)
        super(Query, self).__init__(*args, **kwargs)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Queries'

    def data_time_refresh(self):
        self.lastRefresh = datetime.now()

    def passes_blacklist(self):
        return passes_blacklist(self.final_sql())

    def final_sql(self):
        return swap_params(self.sql, self.params)

    def format_int_in_list(self,L):
        for index, elem in enumerate(L):
            if isinstance(elem, (int, long)):
                L[index] = str("{:,}".format(elem))
        return L

    def try_execute(self):
        """
        A lightweight version of .execute to just check the validity of the SQL.
        Skips the processing associated with QueryResult.
        """
        QueryResult(self.final_sql(), refresh=False)

    def execute(self):


        if self.result_headers is None:
            query_obj = QueryResult(self.final_sql(), refresh=True)
            query_obj.execute_query()

            self.result_headers = json.dumps(query_obj.headers)

            data_list = []
            for tupl in query_obj.data:
                data_list.append(self.format_int_in_list(list(tupl)))
            self.result_data = json.dumps(data_list, cls=AlchemyEncoder)
            self.save()
            return query_obj
        else:
            query_obj = QueryResult(self.final_sql(), refresh=False)
            start_time = time()
            query_obj._data = json.loads(self.result_data)
            query_obj._headers = json.loads(self.result_headers)
            query_obj.duration = ((time() - start_time) * 1000)
            return query_obj

    def available_params(self):
        """
            Merge parameter values into a dictionary of available parameters

        :param param_values: A dictionary of Query param values.
        :return: A merged dictionary of parameter names and values. Values of non-existent parameters are removed.
        """

        p = extract_params(self.sql)
        if self.params:
            shared_dict_update(p, self.params)
        return p

    def get_database_for_query(self):
        return self.database

    def get_absolute_url(self):
        return reverse("query_detail", kwargs={'query_id': self.id})

    def log(self, user):
        log_entry = QueryLog(sql=self.sql, query_id=self.id, run_by_user=user, is_playground=not bool(self.id))
        log_entry.save()

    @property
    def shared(self):
        return self.id in set(sum(app_settings.EXPLORER_GET_USER_QUERY_VIEWS().values(), []))


class QueryLog(models.Model):
    sql = models.TextField()
    query = models.ForeignKey(Query, null=True, blank=True, on_delete=models.SET_NULL)
    is_playground = models.BooleanField(default=False)
    run_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    run_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-run_at']

class ReportTemplate(models.Model):
    title = models.CharField(max_length=100, help_text="Template title")
    description = models.CharField(max_length=100, help_text="Template description")
    sql = models.TextField()
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
            return self.title

    def log(self, user):
        log_entry = QueryLog(sql=self.sql, query_id=self.id, run_by_user=user, is_playground=not bool(self.id))
        log_entry.save()

    def get_absolute_url(self):
        return reverse("template_detail", kwargs={'template_id': self.id})

    @property
    def shared(self):
        return self.id in set(sum(app_settings.EXPLORER_GET_USER_QUERY_VIEWS().values(), []))


class QueryResult(object):
    def __init__(self, sql, refresh):

        if refresh == True:
            self.sql = sql

            res, duration = self.execute_query()

            self.duration = duration

            if hasattr(res,'fetchall'):
                self._data = res.fetchall()
                self._headers = res._metadata.keys
            else:
                self._data = None
                self._headers = None

        else:
            self.sql = sql

            self.duration = 0

            self._data = None

            self._headers = None

    @property
    def data(self):
        return self._data or []

    @property
    def headers(self):
        return self._headers or []

    def execute_query(self):

        conn = get_dataconnection_engine()
        start_time = time()
        try:
            if hasattr(conn,'execute'):
                try:
                    res = conn.execute(self.sql)
                except exc.SQLAlchemyError:
                    res = None
                    pass
            else:
                res = None
        except DatabaseError as e:
            conn.close()
            raise e

        return res, ((time() - start_time) * 1000)


class DataConnection(models.Model):
    """How to connect to a datasource.  This uses sqlalchemy behind the scenes.
    See http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html for details"""

    class Meta:
        verbose_name_plural = "Data Connections"

    name = models.CharField(help_text="Name to identify the dataconnection.", max_length=255,
                            unique=True)
    drivername = models.CharField(max_length=100,
                                  help_text="The name of the database backend. This name will correspond "
                                            "to a module in sqlalchemy/databases or a third party plug-in. Examples: mysql, sqlite")
    username = models.CharField(max_length=300, blank=True)
    password = models.CharField(max_length=300, blank=True)
    host = models.CharField(max_length=300, help_text="The name of the host", blank=True)
    port = models.IntegerField(help_text="The port number", null=True, blank=True)
    database = models.CharField(max_length=300, help_text="The database name")
    active = models.BooleanField(default=True, help_text="Can only have one dataconnection active")

    def get_db_name(self):
        return self.name

    def get_db_flag(self):
        return self.active

    def get_db_connection(self):
        url = sqlalchemy.engine.url.URL(drivername=self.drivername, username=self.username or None,
                                        password=self.password or None, host=self.host or None, port=self.port or None,
                                        database=self.database)
        # Sqlalchemy doesn't seem to let us specify dialect in URL, I guess we have to hack it in??
        s_url = str(url)
        engine = sqlalchemy.create_engine(s_url)
        return engine.connect()

    def get_db_engine(self):
        url = sqlalchemy.engine.url.URL(drivername=self.drivername, username=self.username or None,
                                        password=self.password or None, host=self.host or None, port=self.port or None,
                                        database=self.database)
        s_url = str(url)
        engine = sqlalchemy.create_engine(s_url)
        return engine

    def __unicode__(self):
        return "%s@%s/%s (%s)" % (self.username, self.host, self.database, self.drivername)


class Schema(models.Model):
    schemaName = models.CharField(max_length=300, help_text="Schema Name")
    lastRefresh = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(DataConnection)
    schemaData = models.TextField(blank=True, null=True)


    def __unicode__(self):
        return self.schemaName


    def get_schema_data(self):
        return json.loads(self.schemaData)





