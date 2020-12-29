'''
    Biothings ESQueryHandler Type Tester
'''
import pytest

from biothings.tests.web import BiothingsTestCase


class DiscoveryQueryTest(BiothingsTestCase):

    def test_all(self):
        '''
        [QUERY] Basic functionality
        '''
        res = self.query(q='__all__')
        assert res['total']['value'] == 1

    def test_query(self):
        '''
        [QUERY] Customization by properties
        '''
        self.query(q='mygene')

    def test_102_named_field(self):
        ''' Query named field '''
        self.query(q='tags.name:translator')

    def test_103_match_all(self):
        ''' Query all documents '''
        self.query(q='__all__')

    def test_104_random_score(self):
        ''' Query random documents '''
        res = self.query(q='__any__')
        query_1_id = res['hits'][0]['_id']
        res = self.query(q='__any__')
        query_2_id = res['hits'][0]['_id']
        assert query_1_id != query_2_id

    def test_105_filters(self):
        ''' Query with multiple filters '''
        flt = '{"tags.name.raw":["annotation","variant"],"info.contact.name.raw":["Chunlei Wu"]}'
        res = self.query(q='__all__', filters=flt)
        eq_(len(res['hits']), 3)

    def test_201_special_char(self):
        ''' Handle special characters '''
        self.query(q='translat\xef\xbf\xbd\xef\xbf\xbd', expect_hits=False)
        self.request("query?q=http://example.com/", expect_status=400)

    def test_202_missing_term(self):
        ''' Handle empty request '''
        self.request("query", expect_status=400)

    def test_203_bad_size(self):
        ''' Handle type error '''
        self.request("query?q=__all__&size=my", expect_status=400)

    def test_204_bad_index(self):
        ''' Handle index out of bound '''
        res_0 = self.request('query?q=__all__&fields=_id&size=5').json()
        ids_0 = {hit['_id'] for hit in res_0['hits']}
        res_1 = self.request('query?q=__all__&fields=_id&size=5&from=5').json()
        ids_1 = [hit['_id'] for hit in res_1['hits']]
        for _id in ids_1:
            if _id in ids_0:
                assert False

    # Result Formatting

    def test_301_sources(self):
        ''' Return specified fields '''
        res = self.query(q='__all__', fields='_id,info')
        for hit in res['hits']:
            assert '_id' in hit and 'info' in hit
            assert '_meta' not in hit

    def test_302_size(self):
        ''' Return specified size '''
        res = self.query(q='__all__', size=6)
        eq_(len(res['hits']), 6)

    def test_303_raw(self):
        ''' Return raw ES result '''
        res = self.query(q='__all__', raw=1)
        assert '_shards' in res

    def test_304_query(self):
        ''' Return query sent to ES '''
        res = self.request('query?q=__all__&rawquery=1').json()
        assert "query" in res
        assert "bool" in res["query"]

