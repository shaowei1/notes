#  AssertionError: Dependency rule tried to blank-out primary key column 'file.id' on instance '<File at 0x7fa6ed4e5400>'

```
cascade='all,delete-orphan',
single_parent=True
```
会级联与自己相关联的对象，以自己为准，如果放入backref表示同理

如果使用backref, sqlalchemy 级联时会自动查询父对象，为父对象执行相同操作
