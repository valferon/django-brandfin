import six
from django.test import TestCase

from explorer.tests.factories import SimpleQueryFactory
from explorer.models import QueryLog, Query, QueryResult, ColumnSummary, ColumnHeader


class TestQueryModel(TestCase):
    def test_params_get_merged(self):
        q = SimpleQueryFactory(sql="select '$$foo$$';")
        q.params = {'foo': 'bar', 'mux': 'qux'}
        self.assertEqual(q.available_params(), {'foo': 'bar'})

    def test_query_log(self):
        self.assertEqual(0, QueryLog.objects.count())
        q = SimpleQueryFactory()
        q.log(None)
        self.assertEqual(1, QueryLog.objects.count())
        log = QueryLog.objects.first()
        self.assertEqual(log.run_by_user, None)
        self.assertEqual(log.query, q)
        self.assertFalse(log.is_playground)

    def test_playground_query_log(self):
        query = Query(sql='select 1;', title="Playground")
        query.log(None)
        log = QueryLog.objects.first()
        self.assertTrue(log.is_playground)

    def test_shared(self):
        q = SimpleQueryFactory()
        q2 = SimpleQueryFactory()
        with self.settings(EXPLORER_USER_QUERY_VIEWS={'foo': [q.id]}):
            self.assertTrue(q.shared)
            self.assertFalse(q2.shared)


class TestQueryResults(TestCase):
    def setUp(self):
        self.qr = QueryResult('select 1 as "foo", "qux" as "mux";')

    def test_column_access(self):
        self.qr._data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(self.qr.column(1), [2, 5, 8])

    def test_headers(self):
        self.assertEqual(str(self.qr.headers[0]), "foo")
        self.assertEqual(str(self.qr.headers[1]), "mux")

    def test_data(self):
        self.assertEqual(self.qr.data, [[1, "qux"]])

    def test_unicode_detection(self):
        self.assertEqual(self.qr._get_unicodes(), [1])

    def test_uncode_with_nulls(self):
        self.qr._headers = [ColumnHeader('num'), ColumnHeader('char')]
        self.qr._description = [("num",), ("char",)]
        self.qr._data = [[2, six.u("a")], [3, None]]
        self.qr.process()
        self.assertEqual(self.qr.data, [[2, b"a"], [3, None]])

    def test_summary_gets_built(self):
        self.qr.process()
        self.assertEqual(len([h for h in self.qr.headers if h.summary]), 1)
        self.assertEqual(str(self.qr.headers[0].summary), "foo")
        self.assertEqual(self.qr.headers[0].summary.stats["Sum"], 1.0)

    def test_summary_gets_built_for_multiple_cols(self):
        self.qr._headers = [ColumnHeader('a'), ColumnHeader('b')]
        self.qr._description = [("a",), ("b",)]
        self.qr._data = [[1, 10], [2, 20]]
        self.qr.process()
        self.assertEqual(len([h for h in self.qr.headers if h.summary]), 2)
        self.assertEqual(self.qr.headers[0].summary.stats["Sum"], 3.0)
        self.assertEqual(self.qr.headers[1].summary.stats["Sum"], 30.0)

    def test_numeric_detection(self):
        self.assertEqual(self.qr._get_numerics(), [0])

    def test_transforms_are_identified(self):
        self.qr._headers = [ColumnHeader('foo')]
        got = self.qr._get_transforms()
        self.assertEqual([(0, '<a href="{0}">{0}</a>')], got)

    def test_transform_alters_row(self):
        self.qr._headers = [ColumnHeader('foo'), ColumnHeader('qux')]
        self.qr._data = [[1, 2]]
        self.qr.process()
        self.assertEqual(['<a href="1">1</a>', 2], self.qr._data[0])

    def test_multiple_transforms(self):
        self.qr._headers = [ColumnHeader('foo'), ColumnHeader('bar')]
        self.qr._data = [[1, 2]]
        self.qr.process()
        self.assertEqual(['<a href="1">1</a>', 'x: 2'], self.qr._data[0])

    def test_get_headers_no_results(self):
        self.qr._description = None
        self.assertEqual([ColumnHeader('--')][0].title, self.qr._get_headers()[0].title)


class TestColumnSummary(TestCase):
    def test_executes(self):
        res = ColumnSummary('foo', [1, 2, 3])
        self.assertEqual(res.stats, {'Min': 1, 'Max': 3, 'Avg': 2, 'Sum': 6, 'NUL': 0})

    def test_handles_null_as_zero(self):
        res = ColumnSummary('foo', [1, None, 5])
        self.assertEqual(res.stats, {'Min': 0, 'Max': 5, 'Avg': 2, 'Sum': 6, 'NUL': 1})

    def test_empty_data(self):
        res = ColumnSummary('foo', [])
        self.assertEqual(res.stats, {'Min': 0, 'Max': 0, 'Avg': 0, 'Sum': 0, 'NUL': 0})
