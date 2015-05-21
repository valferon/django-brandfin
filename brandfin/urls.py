from django.conf.urls import patterns, url

from views import QueryView, CreateQueryView, PlayQueryView, DeleteQueryView, ListQueryView, ListQueryLogView, RefreshQueryView, TemplateView, CreateTemplateView, DeleteTemplateView


urlpatterns = patterns('',
                       url(r'template_(?P<template_id>\d+)/$', TemplateView.as_view(), name='template_detail'),
                       url(r'template_(?P<pk>\d+)/delete$', DeleteTemplateView.as_view(), name='template_delete'),
                       url(r'new_template/$', CreateTemplateView.as_view(), name='template_create'),
                       url(r'(?P<query_id>\d+)/$', QueryView.as_view(), name='query_detail'),
                       url(r'(?P<query_id>\d+)/download$', 'brandfin.views.download_query', name='query_download'),
                       url(r'(?P<query_id>\d+)/csv', 'brandfin.views.view_csv_query', name='query_csv'),
                       url(r'(?P<pk>\d+)/delete$', DeleteQueryView.as_view(), name='query_delete'),
                       url(r'(?P<query_id>\d+)/refresh$', RefreshQueryView.as_view(), name='query_refresh'),
                       url(r'new/$', CreateQueryView.as_view(), name='query_create'),
                       url(r'play/$', PlayQueryView.as_view(), name='explorer_playground'),
                       url(r'csv$', 'brandfin.views.download_csv_from_sql', name='generate_csv'),
                       url(r'schema/$', 'brandfin.views.schema', name='explorer_schema'),
                       url(r'logs/$', ListQueryLogView.as_view(), name='explorer_logs'),
                       url(r'format/$', 'brandfin.views.format_sql', name='format_sql'),
                       url(r'^$', ListQueryView.as_view(), name='explorer_index'),
                       )
