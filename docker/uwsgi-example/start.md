```shell
cd app && uwsgi --http :5000 -w app.main
```

如果想在 Python 代码更改时进行 autoreload，使用

```shell
cd app && uwsgi --http :5000 -w app.main --py-autoreload=1
```
