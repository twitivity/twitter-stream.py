import os
import json

import requests


class Stream:
    _protocol: str = "https:/"
    _host: str = "api.twitter.com"
    _version: str = "2"
    _product: str = "tweets/search"

    def api(
        self, method: str, endpoint: str, data: dict = None, stream: bool = None
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
                )
                return response
        except Exception as e:
            raise e


class FilteredStream(Stream):
    def add_rule(self, data: dict) -> json:
        return self.api(method="POST", endpoint="stream/rules", data=data).json()

    def get_rules(self) -> json:
        return self.api(method="GET", endpoint="stream/rules").json()

    def delete_rule(self, data: dict) -> json:
        return self.api(method="POST", endpoint="stream/rules", data=data)

    def connect(self):
        try:
            response = self.api("GET", endpoint="stream", stream=True)
            response.raise_for_status()
            for response_lines in response.iter_lines():
                if response_lines:
                    yield json.loads(response_lines)
        except Exception as e:
            raise e