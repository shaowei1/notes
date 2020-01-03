# DatabaseError

```
sqlalchemy.exc.DatabaseError: (mysql.connector.errors.DatabaseError) 1273 (HY000): Unknown collation: 'utf8mb4_0900_ai_ci'
```

本地数据库使用的collation 包含 utf8mb4_general_ci(mysql 5.7 指定chaset=utf8mb4) 和 utf8_general_ci(mysql 5.7没指定chaset默认) 两种, 但是mysqlconnector 指定了charset

```
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'

```

Utf8_general_ci 指utf8mb3 所以不兼容报错

- mysql 8.0 默认utf8mb4

