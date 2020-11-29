import json
import os

import requests


class API:
    _protocol: str = "https:/"
    _host: str = "api.twitter.com"
    _version: str = "2"
    _product: str = None
    _endpoint: str = None
    _has_params: bool = None
    _params: dict = {}
    _stream: bool = None
    _data: dict = None
    _exclude: list = []

    def api(
        self,
        method: str,
        endpoint: str = None,
        data: dict = None,
        stream: bool = None,
        params: dict = None,
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
                        "Authorization": f"Bearer {os.environ['BEARER_TOKEN']}",
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

            response = self.api(
                method="GET",
                endpoint=self._endpoint,
                stream=self._stream,
                params=self._params,
            )
            response.raise_for_status()
            for response_lines in response.iter_lines():
                yield json.loads(response_lines)
        except Exception as e:
            raise e


class FilteredStream(API):
    _product = "tweets"
    _endpoint = "search/stream"
    _stream = True

    def add_rule(self, data: dict) -> json:
        return self.api(method="POST", endpoint="search/stream/rules", data=data).json()

    def get_rules(self) -> json:
        return self.api(method="GET", endpoint="search/stream/rules").json()

    def delete_rule(self, data: dict):
        return self.api(method="POST", endpoint="search/stream/rules", data=data).json()

    def delete_all_rules(self) -> json:
        try:
            rules = self.get_rules().json()
            ids = list(map(lambda rule: rule["id"], rules["data"]))
            return self.delete_rule({"delete": {"ids": ids}})
        except Exception as e:
            pass


class SampledStream(API):
    _product = "tweets"
    _endpoint = "sample/stream"
    _has_params = True
    _stream = True


class RecentSearch(API):
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
