# query all foreign keys
```

select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where table_schema = 'merchant'



```

sqlacodegen mysql+pymysql://root:xinyue@192.168.15.179/merchant > model.py
