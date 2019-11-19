# convert OrderDict to dict

```python
import json
from collections import OrderedDict

input_data = OrderedDict({"key": "value"})
result = json.loads(json.dumps(input_data))
```
