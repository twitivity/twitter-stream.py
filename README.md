# twitter-stream.py

# Filtered Stream

## Quickstart
![](assets/quickstart.png)

### Adding Rules
```python
>>> import json
>>> from twitter_stream import FilteredStream

>>> stream = FilteredStream()
>>> rules = {"add": [{'value': 'from: twitivitydev'}]}
>>> print(json.dumps(stream.add_rule(data=rules), indent=4))
```

### Deleting Rules
```python
>>> import json
>>> from twitter_stream import FilteredStream

>>> stream = FilteredStream()
>>> response = stream.delete_rule({"delete": {"ids": ['1331486534579589120']}})
>>> print(response)
```

### Get Rules
```python
>>> import json
>>> from twitter_stream import FilteredStream

>>> stream = FilteredStream()
>>> print(json.dumps(stream.get_rules(), indent=4, sort_keys=True))
```

### Stream
```python
>>> import json
>>> from twitter_stream import FilteredStream

>>> stream = FilteredStream()
>>> for tweet in stream.connect():
       print(json.dumps(tweet, indent=4))
```

## Installation
```bash
~$ pip3 install twitter-stream.py
```


