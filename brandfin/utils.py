import functools
import csv
import json
import re
import string
import datetime
from decimal import Decimal

import django.db
from django.http import HttpResponse
import sqlparse
import app_settings

# noinspection PyUnresolvedReferences
from six.moves import cStringIO


EXPLORER_PARAM_TOKEN = "$$"

# SQL Specific Things
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return super(AlchemyEncoder, self).default(obj)

def query_data_to_list(data_result):
    my_list = []
    for row in data_result:
        my_list.append([str(elem).encode('utf8') for elem in row])
    return my_list


def query_header_to_list(header_result):
    my_list = []
    for row in header_result:
        my_list.append(str(row).encode('utf8'))
    return my_list


def decode_json_to_list(json_obj):
    """
    :rtype : list
    """
    jsondec = json.decoder.JSONDecoder()
    my_list = jsondec.decode(json_obj)
    return my_list


def passes_blacklist(sql):
    clean = functools.reduce(lambda sql, term: sql.upper().replace(term, ""), app_settings.EXPLORER_SQL_WHITELIST, sql)
    return not any(write_word in clean.upper() for write_word in app_settings.EXPLORER_SQL_BLACKLIST)


def get_dataconnection_engine():
    from .models import DataConnection
    engine = object
    db_list = DataConnection.objects.all()
    for db in db_list:
        if DataConnection.get_db_flag(db) == True:
            engine = DataConnection.get_db_engine(db)
    return engine

def get_dataconnection_active():
    from .models import DataConnection
    db_list = DataConnection.objects.all()
    for db in db_list:
        if DataConnection.get_db_flag(db) == True:
            return db
        else:
            return None

def _format_sqlalch_field(field):
    return (field['name'], str(field['type']))


def _format_field(field):
    return (field.get_attname_column()[1], field.get_internal_type())


def param(name):
    return "%s%s%s" % (EXPLORER_PARAM_TOKEN, name, EXPLORER_PARAM_TOKEN)


def swap_params(sql, params):
    p = params.items() if params else {}
    for k, v in p:
        sql = sql.replace(param(k), str(v))
    return sql


def extract_params(text):
    regex = re.compile("\$\$([a-zA-Z0-9_|-]+)\$\$")
    params = re.findall(regex, text)
    return dict(zip(params, ['' for i in range(len(params))]))


def write_csv(headers, data):
    csv_data = cStringIO()
    writer = csv.writer(csv_data)
    writer.writerow(headers)
    for row in data:
        writer.writerow(row)
    return csv_data.getvalue()


def get_filename_for_title(title):
    # build list of valid chars, build filename from title and replace spaces
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in title if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename


def build_stream_response(query):
    data = csv_report(query)
    response = HttpResponse(data, content_type='text')
    return response


def build_download_response(query):
    data = csv_report(query)
    response = HttpResponse(data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (
        get_filename_for_title(query.title)
    )
    response['Content-Length'] = len(data)
    return response


def csv_report(query):
    try:
        res = query.execute()
        return write_csv(res.headers, res.data)
    except django.db.DatabaseError as e:
        return str(e)


# Helpers
from django.contrib.admin.forms import AdminAuthenticationForm

from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME


def safe_admin_login_prompt(request):
    defaults = {
        'template_name': 'admin/login.html',
        'authentication_form': AdminAuthenticationForm,
        'extra_context': {
            'title': 'Log in',
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        },
    }
    return login(request, **defaults)


def shared_dict_update(target, source):
    for k_d1 in target:
        if k_d1 in source:
            target[k_d1] = source[k_d1]
    return target


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except ValueError:
        return default


def safe_json(val):
    try:
        return json.loads(val)
    except ValueError:
        return None


def get_int_from_request(request, name, default):
    val = request.GET.get(name, default)
    return safe_cast(val, int, default) if val else None


def get_json_from_request(request, name):
    val = request.GET.get(name, None)
    return safe_json(val) if val else None


def url_get_rows(request):
    return get_int_from_request(request, 'rows', app_settings.EXPLORER_DEFAULT_ROWS)


def url_get_query_id(request):
    return get_int_from_request(request, 'query_id', None)


def url_get_template_id(request):
    return get_int_from_request(request, 'template_id', None)



def url_get_log_id(request):
    return get_int_from_request(request, 'querylog_id', None)


def url_get_params(request):
    return get_json_from_request(request, 'params')


def user_can_see_query(request, kwargs):
    if not request.user.is_anonymous() and 'query_id' in kwargs:
        allowed_queries = app_settings.EXPLORER_GET_USER_QUERY_VIEWS().get(request.user.id, [])
        return int(kwargs['query_id']) in allowed_queries
    return False


def fmt_sql(sql):
    return sqlparse.format(sql, reindent=True, keyword_case='upper')

