import json
import os

import requests
import yaml

from requests_oauthlib import OAuth1
from functools import wraps


def auth(filename="~/.twitter-keys.yaml"):
    def inner_function(func):
        @wraps(func)
        def wrapper(args, **kwargs):
            try:
                with open(os.path.expanduser(filename)) as credentials:
                    credentials = yaml.safe_load(credentials)["keys"]
            except (FileNotFoundError, KeyError) as exception:
                raise exception
            else:
                kwargs["auth"] = credentials
            return func(args, **kwargs)

        return wrapper

    return inner_function


class API:
    _protocol: str = "https:/"
    _host: str = "api.twitter.com"
    _version: str = "2"
    _product: str = None
    _endpoint: str = None
    _has_params: bool = None
    _pagination: bool = False
    _params: dict = {}
    _stream: bool = None
    _data: dict = None
    _exclude: list = []

    @auth()
    def api(
        self,
        method: str,
        endpoint: str = None,
        data: dict = None,
        stream: bool = None,
        params: dict = None,
        **kwargs,
    ) -> json:
        try:
            with requests.Session() as r:
                response = r.request(
                    url="/".join(
                        [
                            self._protocol,
                            self._host,
                            self._version,
                            self._product,
                            endpoint,
                        ]
                    ),
                    method=method,
                    headers={
                        "Content-type": "application/json",
                        "Authorization": f"Bearer {kwargs['auth']['bearer_token']}",
                    },
                    json=data,
                    stream=stream,
                    params=params,
                )
                return response
        except Exception as e:
            raise e

    def _query(self) -> dict:
        self._params = {}
        try:
            [
                self._params.update(
                    {v.replace("_", "."): ",".join(self.__class__.__dict__[v])}
                )
                for v in self.__class__.__dict__
                if not callable(getattr(self, v))
                and not v.startswith("__")
                and v not in self._exclude
            ]
            return self._params
        except Exception as e:
            raise e

    def connect(self) -> dict:
        try:
            if self._has_params:
                self._params = self._query()

            data = None

            while True:
                response = self.api(
                    method="GET",
                    endpoint=self._endpoint,
                    stream=self._stream,
                    params=self._params,
                )
                response.raise_for_status()
                for response_lines in response.iter_lines():
                    data = json.loads(response_lines)
                    yield data

                if not self._pagination:
                    break
                self._params["next_token"] = data["meta"]["next_token"]

        except Exception as e:
            raise e


class FilteredStream(API):
    """
    Endpoint: /2/tweets/search/stream
    replaces legacy endpoint v1.1 statuses/filter
    """

    _product = "tweets"
    _endpoint = "search/stream"
    _stream = True

    def add_rule(self, data: dict) -> json:
        """Add or Remove upto 25 rules.
        /2/tweets/search/stream/rules

        List of Rules: (https://developer.twitter.com/en/docs/
        twitter-api/tweets/filtered-stream/integrate/build-a-rule)

        :params data: a dict with a list of rules
        :return: json

        Usage:

        stream = FilteredStream()
        rules = {
            "add": [
                {"value": "dog has: images", "tag": "dog pictures"}
            ]
        }
        stream.add_rule(data=rules)
        """
        return self.api(method="POST", endpoint="search/stream/rules", data=data).json()

    def get_rules(self) -> json:
        """Retrieve your stream's rules
        /2/tweets/search/stream/rules
        :return: json
        """
        return self.api(method="GET", endpoint="search/stream/rules").json()

    def delete_rule(self, data: dict):
        """Add or Remove upto 25 rules.
        /2/tweets/search/stream/rules

        List of Rules: (https://developer.twitter.com/en/docs/
        twitter-api/tweets/filtered-stream/integrate/build-a-rule)

        :params data: a dict with a list rule Ids
        :return: json

        Usage:

        stream = FilteredStream()
        rules = {
            "delete": {
                "ids": ['1331486534579589120'] # example id
            }
        }
        """
        return self.api(method="POST", endpoint="search/stream/rules", data=data).json()

    def delete_all_rules(self) -> json:
        """Deletes all your rules automatically"""
        try:
            rules = self.get_rules().json()
            ids = list(map(lambda rule: rule["id"], rules["data"]))
            return self.delete_rule({"delete": {"ids": ids}})
        except Exception as e:
            pass


class SampledStream(API):
    """Endpoint: /2/tweets/sample/stream
    Replacement for: v1.1 statuses/sample

    Subclasses the API class. Overrides variables
    `_product`, `_endpoint`, '_has_params', and
    '_stream'. The inherited `connect()` method
    from the super class does the streaming.

    The inherited connect method also helps in
    evaluating and constructing queries for sampled
    stream.

    List of query parameters
    (https://developer.twitter.com/en/docs/twitter-api/
    tweets/sampled-stream/api-reference/get-tweets-sample-stream)


    Usage:

    Name the query parameter and assign their values in a list.
    The `connect()` method recognizes the query parameters and
    and starts streaming.


    class Stream(SampledStream):
        user_fields = ['name', 'location', 'public_metrics']
        expansions = ['author_id']

    stream = Stream()

    for tweets in stream.connect():
        print(json.dumps(tweets, indent=4, sort_keys=True)))


    """

    _product = "tweets"
    _endpoint = "sample/stream"
    _has_params = True
    _stream = True


class RecentSearch(API):
    """Endpoint: /2/tweets/search/recent
    Legacy endpoint: v1.1 search/tweets

    Behaves the same way as SampledStream.

    List of query parameters
    (https://developer.twitter.com/en/docs/twitter-api/
     tweets/search/api-reference/get-tweets-search-recent)

    """

    _product = "tweets"
    _endpoint = "search/recent"
    _has_params = True
    _stream = True
    _exclude = [
        "end_time",
        "max_results",
        "next_token",
        "since_id",
        "start_time",
        "until_id",
    ]
    _pagination = True


class TweetLookUp(API):
    """Endpoint: /2/tweets
    Legacy endpoint: v1.1 statuses/show, v1.1 status/lookup

    List of query parameters:
    (https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference)
    """

    @auth()
    def get(self, **kwargs) -> json:
        response = requests.request(
            method="GET",
            url="https://api.twitter.com/2/tweets",
            params=self._query(),
            headers={
                "Content-type": "application/json",
                "Authorization": f"Bearer {kwargs['auth']['bearer_token']}",
            },
        )
        return response.json()


class UserLookUp(API):
    """Endpoint /2/users
    Legacy Endpoint v1.1 users/lookup
    """

    def _query(self) -> dict:
        try:
            _params: dict = {}
            _exclude: list = ["max_results"]
            for v in self.__class__.__dict__:
                if v in _exclude:
                    _params.update({v: ",".join(self.__class__.__dict__[v])})
                if (
                    not callable(getattr(self, v))
                    and not v.startswith("__")
                    and v not in _exclude
                ):
                    _params.update(
                        {v.replace("_", "."): ",".join(self.__class__.__dict__[v])}
                    )
        except Exception as e:
            raise e
        return _params

    @auth()
    def get(
        self,
        endpoint: str = "https://api.twitter.com/2/users",
        query_params=True,
        **kwargs,
    ) -> json:
        return requests.request(
            method="GET",
            url=endpoint,
            params=self._query() if query_params else None,
            headers={
                "Content-type": "application/json",
                "Authorization": f"Bearer {kwargs['auth']['bearer_token']}",
            },
        ).json()

    def get_by_usernames(
        self, endpoint: str = "https://api.twitter.com/2/users/by", query_params=True
    ) -> json:
        return self.get(endpoint=endpoint, query_params=query_params)

    def get_details_by_username(
        self,
        data: str,
        endpoint: str = "https://api.twitter.com/2/users/by/username",
        query_params=True,
    ):
        endpoint = endpoint + "/" + data
        return self.get(endpoint=endpoint, query_params=query_params)

    @auth()
    def followers(self, username, **kwargs):
        try:
            user_id = self.get_details_by_username(username, query_params=False)[
                "data"
            ]["id"]
            params = self._query()
            while True:
                data = requests.get(
                    url=f"https://api.twitter.com/2/users/{user_id}/followers",
                    params=params,
                    headers={
                        "Content-type": "application/json",
                        "Authorization": f"Bearer {kwargs['auth']['bearer_token']}",
                    },
                )
                print(data.url)
                data.raise_for_status()
                for response_lines in data.iter_lines():
                    data = json.loads(response_lines)
                    yield data

                params["pagination_token"] = data["meta"]["next_token"]

        except KeyError as k:
            pass
        except Exception as e:
            raise e


def hide_replies(tweet: str, hidden: dict) -> json:
    """https://api.twitter.com/2/tweets/:id/hidden
    Hides specific tweets from a conversation
    :params: tweet: str = url  of the tweet to hide
    :params: hidden: dict = {"hidden: True}

    :returns json

    Usage:

    hide_replies(
        tweet = 'https://twitter.com/saadmanrafat_/status/1328288598106443776',
        {"hidden": True}
    )

    response =
    {
        "data": {
            "hidden": true
        }
    }
    """
    try:
        with open(os.path.expanduser("~/.twitter-keys.yaml")) as credentials:
            credentials = yaml.safe_load(credentials)["keys"]
    except (FileNotFoundError, KeyError) as e:
        raise e

    auth = OAuth1(
        client_key=credentials["consumer_key"],
        client_secret=credentials["consumer_secret"],
        resource_owner_key=credentials["access_token"],
        resource_owner_secret=credentials["access_token_secret"],
        signature_type="auth_header",
    )
    tweet_id = tweet.split("/")[-1]
    response = requests.put(
        url=f"https://api.twitter.com/2/tweets/{tweet_id}/hidden",
        headers={"Content-Type": "application/json"},
        auth=auth,
        data=json.dumps(hidden),
    )
    return json.dumps(response.json(), indent=4)
