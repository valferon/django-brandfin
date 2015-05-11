# django-brandfin
Modified version of django-sql-explorer allowing to specify external databases.

Beta version

* Django app that allows you to connect to a database using SqlAlchemy to get the database schema and run queries against that database and save it as a report.

- Tested against Postgresql
- Store the report query result in the django database as Json for quick display and with 'Refresh Data' function to re-run the query against the DB


Todo

- add a command to refresh reports by running all queries against the DB
- include a relation between db datasource and reports to allow multiple database sources ( currently only one active datasource at a time)
- add helpers to create query (sum,....)

