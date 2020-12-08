import json
import os
from unittest import TestCase
from twitter_stream import hide_replies

os.environ['API_KEY'] = "API_KEY"
os.environ['API_KEY_SECRET'] = "API_KEY_SECRET"
os.environ['ACCESS_TOKEN'] = "ACCESS_TOKEN"
os.environ['ACCESS_TOKEN_SECRET'] = "ACCESS_TOKEN_SECRET"


class TestHideReplies(TestCase):

    def test_reply_hide(self):
        response = hide_replies(
            tweet="https://twitter.com/saadmanrafat_/status/1328288598106443776",
            hidden={"hidden": True},
        )
        response = json.loads(response)
        self.assertTrue(response["data"]["hidden"], True)

    def test_reply_unhide(self):
        response = hide_replies(
            tweet="https://twitter.com/saadmanrafat_/status/1328288598106443776",
            hidden={"hidden": False},
        )
        response = json.loads(response)
        self.assertFalse(response["data"]["hidden"], False)