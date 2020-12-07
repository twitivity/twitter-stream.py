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

## Hide Replies
```angular2html
~$ export $API_KEY=API_KEY
~$ export $API_KEY_SECRET=API_KEY_SECRET
~$ export $ACCESS_TOKEN=ACCESS_TOKEN
~$ export $ACCESS_TOKEN_SECRET=ACCESS_TOKEN_SECRET
```

```python



from twitter_stream import hide_replies

response = hide_replies(
    tweet="https://twitter.com/saadmanrafat_/status/1327509412374740993",
    hidden={"hidden": True} # {"hidden": False } in case of unhide
    
)
print(response)

OUTPUT:

{
    "data": {
        "hidden": true
    }
}


```
