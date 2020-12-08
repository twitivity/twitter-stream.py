
<p align="center"><a href="https://github.com/twitivity/twitter-stream.py"><img src="/assets/twitte-stream.png"/></a></p>

<h1 align="center">twitter-stream.py</h1>
<p align="center">:snake: Python Client For Twitter API v2</p>

<p align="center">
	<a href="https://github.com/twitivity/twitter-stream.py"><img src="https://img.shields.io/pypi/pyversions/twitter-stream.py" height="20"/></a>
    <a href="https://github.com/twitivity/twitter-stream.py"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2" alt="Twitter APi V2" height="20"/></a>
        <a href="https://github.com/twitivity/twitter-stream.py"><img src="https://img.shields.io/pypi/l/twitter-stream.py" alt="Twitter APi V2" height="20"/></a>
</p><br/><br/>

# :rocket: Why Twitter Stream ?
[Twitter-Stream.py](https://github.com/twitivity/twitter-stream.py) a python API client for Twitter API v2 now supports 
`FilteredStream`, `SampledStream`, `RecentSearch`, `TweetLookUp`, and  `UserLookUp`. It makes it easier to get started with Twitter's New API. Let's see an example of how `twitter-stream.py` handles `SampledStream`. Sampled Stream delivers about 1% of Twitter's publicly available tweets in real-time and paints a picture of general sentiments, recent trends, and global events.

```python
# sampled_stream.py

import json
from twitter_stream import SampledStream

class Stream(SampledStream):
    user_fields = ['name', 'location', 'public_metrics']
    expansions = ['author_id']
    tweet_fields = ['created_at']

stream = Stream()
for tweet in stream.connect():
    print(json.dumps(tweet, indent=4))
```

Is this all you have to do to start streaming? Yes. Are these all the data points available to you? No. Let's discuss `line number 5-7`. [Twitter's Official Documentation](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/api-reference/get-tweets-sample-stream) lists an elaborate set of query parameters. You can use these queries to get the data you need. We are subclassing `SampledStream` and carefully constructing clear and eloquent queries in `line 5-7`. And you can do this for all the query parameters listed in the `SampledStream` [API Reference](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/api-reference/get-tweets-sample-stream).

To get more insights into other API endpoints. Visit the [examples](https://github.com/twitivity/twitter-stream.py/tree/master/examples) folder and our documentations [twitivity.dev](http://twitivity.dev/docs/).

# Installation and Setup
```
~$ pip3 install twitter-stream.py
```

