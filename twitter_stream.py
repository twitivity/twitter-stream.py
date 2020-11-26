import os
import json

import requests


class Stream:
    _protocol: str = "https:/"
    _host: str = "api.twitter.com"
    _version: str = "2"
    _product: str = "tweets/search"

    def api(
        self,
        method: str,
        endpoint: str,
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

    def connect(self) -> dict:
        try:
            response = self.api("GET", endpoint="stream", stream=True)
            response.raise_for_status()
            for response_lines in response.iter_lines():
                yield json.loads(response_lines)
        except Exception as e:
            pass


class FilteredStream(Stream):
    def add_rule(self, data: dict) -> json:
        return self.api(method="POST", endpoint="stream/rules", data=data).json()

    def get_rules(self) -> json:
        return self.api(method="GET", endpoint="stream/rules").json()

    def delete_rule(self, data: dict) -> json:
        return self.api(method="POST", endpoint="stream/rules", data=data)


class SampledStream(Stream):

    _product = "tweets/sample"

    def connect(self) -> dict:
        try:
            params: dict = {}
            [
                params.update(
                    {v.replace("_", "."): ",".join(self.__class__.__dict__[v])}
                )
                for v in self.__class__.__dict__
                if not callable(getattr(self, v)) and not v.startswith("__")
            ]
            response = self.api("GET", endpoint="stream", stream=True, params=params)
            response.raise_for_status()
            for response_lines in response.iter_lines():
                yield json.loads(response_lines)
        except Exception as e:
            raise e
