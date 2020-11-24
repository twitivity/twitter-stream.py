# twitter-stream.py

# Quickstart

```python
import json
from twitter_stream import FilteredStream

if __name__ == '__main__':
    stream = FilteredStream()
    rules: list = [
        {"value": "dog has:images", "tag": "dog pictures"},
        {"value": "cat has:images -grumpy", "tag": "cat pictures"}
    ]
    
    # add the rules
    stream.add_rule(data={"add": rules})
    
    # stream
    for tweet in stream.connect():
        print(json.dumps(tweet, indent=4, sort_keys=True))
        
```

## Demo

<img src="assets/demo.gif" width="650" height="600" />


## Installation
```
~$ pip3 install twitter-stream.py
```
