# twitter-stream.py

## Quickstart
```python
import json
from twitter_stream import FilteredStream

if __name__ == "__main__":
    filter_stream = FilteredStream()
    for data in filter_stream.connect():
        print(json.dumps(data, indent=4, sort_keys=True))
```

## Installation
```
~$ pip3 install twitter-stream.py
```