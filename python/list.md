#list flat

```
a=[[1,2],[3,4],[5,6]]
print [j for i in li for j in i]
#or
from itertools import chain
print list(chain(*a))
#or
import itertools
a = [[1,2,3],[4,5,6], [7], [8,9]]
out = list(itertools.chain.from_iterable(a))
#or
a=[[1,2],[3,4],[5,6]]
t=[]
[t.extend(i) for i in a]
print t
#or
a=[[1,2],[3,4],[5,6]]
print sum(a,[])
#or
reduce(lambda x, y: x+ y, a)


## 递归的方法比较容易理解
def expand_list(nested_list):
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in expand_list(item):
                yield sub_item
        else:
            yield item

## 在stackoverflow看到大牛的列表生成式版本
func = lambda x: [y for l in x for y in func(l)] if type(x) is list else [x]

```

:tada: :fireworks:
