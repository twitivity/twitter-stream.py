<p align="center"><a href="https://github.com/twitivity/twitter-stream.py"><img src="https://avatars1.githubusercontent.com/u/74627580?s=400&u=2a5502073d9f5d79b08aeac58df8171b262cb010&v=4" height="120"/></a></p>

<h1 align="center">twitter-stream.py</h1>
<p align="center">Python Client For Twitter API v2</p>

<p align="center">
	<a href="https://github.com/twitivity/twitter-stream.py"><img src="https://img.shields.io/pypi/pyversions/twitter-stream.py" height="20"/></a>
    <a href="https://github.com/twitivity/twitter-stream.py"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2" alt="Twitter APi V2" height="20"/></a>
        <a href="https://github.com/twitivity/twitter-stream.py"><img src="https://img.shields.io/pypi/l/twitter-stream.py" alt="Twitter APi V2" height="20"/></a>
</p><br/><br/>



# :rocket: Quick Start

## Sampled Stream

Construct cleaner and concise queries. Subclass SampledStream, name your desired query parameters, and assign their values in a list. twitter-stream.py will take care of the rest.
[Here are the list of query parameters](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/api-reference/get-tweets-sample-stream)

```python
# sampled_stream.py

import json
from twitter_stream import SampledStream

class Stream(SampledStream):
    user_fields = ['name', 'location', 'public_metrics']
    expansions = ['author_id']
    tweet_fields = ['created_at', 'geo']

stream = Stream()
for tweet in stream.connect():
    print(json.dumps(tweet, indent=4))
```

## Recent Stream
Get Recent Stream Based on your queries. [Checkout the list of query parameters for Recent Stream](https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent)
```python
# recent_search.py

import json
from twitter_stream import RecentSearch

class Stream(RecentSearch):
    query = ['python']
    max_results = ['10']
    tweet_fields = ['created_at', 'lang', 'conversation_id']

stream = Stream()

for tweet in stream.connect():
    print(json.dumps(tweet, indent=4))
```

## Filtered Stream

For `FilteredStream` documentations on adding, deleting and retriving rules can be found here.
[twitivity.dev/docs](https://twitivity.dev/docs/twitter-stream.py/)

```python
# filtered_stream.py

import json
from twitter_stream import FilteredStream

rules: list = [
    {"value": "dog has:images", "tag": "dog pictures"},
    {"value": "cat has:images -grumpy", "tag": "cat pictures"}
]
stream = FilteredStream()

stream.add_rule(data={"add": rules})

for tweet in stream.connect():
    print(json.dumps(tweet, indent=4))
```

## TweetLookUp

Returns information about a Tweet or group of Tweets [List of Query Parameters](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference)
```python
# tweet_lookup.py

import json
from twitter_stream import TweetLookUp

class Tweet(TweetLookUp):
    ids = ['1261326399320715264','1278347468690915330']
    expansions = ['author_id']
    tweet_rules = ['created_at']
    user_fields = ['username', 'verified']

tweet = Tweet()
print(json.dumps(tweet, indent=4, sort_keys=True))
```

## UserLookUp
Returns a variety of information about one or more users specified by the requested **IDs**.
[List of Query Parameters](https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users)

```python
# tweet_lookup.py

import json
from twitter_stream import UserLookUp

class User(UserLookUp):
    ids = ['2244994945', '783214']
    expansions = ["pinned_tweet_id"]
    user_fields = ["created_at"]
    tweet_fields = ["created_at"]

user = User()
print(json.dumps(user.get(), indent=4))
```

Returns a variety of information about one or more users specified by their **usernames**.
[List of Query Parameters](https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by)
```python
# tweet_lookup_by_username.py

import json
from twitter_stream import UserLookUp

class User(UserLookUp):
    usernames = ['TwitterDev', 'Twitter']
    expansions = ["pinned_tweet_id"]
    user_fields = ["created_at"]
    tweet_fields = ["created_at"]

user = User()
print(json.dumps(user.get_by_usernames(), indent=4))
```

Returns a variety of information about one or more users specified by their usernames.
[List of Query Parameters](https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by-username-username)
```python
# tweet_detail_lookup_by_username.py
import json
from twitter_stream import UserLookUp

class User(UserLookUp):
    expansions = ["pinned_tweet_id"]
    user_fields = ["created_at"]
    tweet_fields = ["created_at"]

user = User()
print(json.dumps(user.get_details_by_username("TwitterDev"), indent=4))
```

### Bearer Token
```
~$ export BEARER_TOKEN=BEARER TOKEN
```



## Installation
```python
~$ pip3 install twitter-stream.py
```
<br>

<p align="center"><a href="https://github.com/twitivity/twitter-stream.py"><img src="http://randojs.com/images/barsSmall.gif" alt="Animated footer bars" width="100%"/></a></p>
