import unittest

from twitter_stream import RecentSearch


class TestRecentSearch(unittest.TestCase):

    class Search(RecentSearch):
        query = ['python']
        max_results = ['10']
        tweet_fields = ['created_at', 'lang', 'conversation_id']

    def setUp(self) -> None:
        self.search = self.Search()
        for tweet in self.search.connect():
            self._response = tweet

    def test_result_count(self):
        assert self._response['meta']['result_count'] == 10

    def test_response_has_created_at(self):
        self.assertTrue(self._response['data'][0]['created_at'], 'created_at')

    def test_response_has_lang(self):
        self.assertTrue(self._response['data'][0]['lang'], 'lang')

    def test_response_has_conversation_id(self):
        self.assertTrue(self._response['data'][0]['conversation_id'], 'conversation_id')

