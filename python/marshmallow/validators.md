```python
class WashingSymbolCollectionSerializer(ModelSerializer):
    account_id = fields.Integer(load_only=True)

    class Meta:
        # from marshmallow import INCLUDE, EXCLUDE
        # unknown = INCLUDE
        # nested字段，如果不在Meta fields 里面最后一个, post或者put --> unknown field错误, 如果在里面dump 没有会报错
        # 如果放在Schema的类变量使用Nested field，一起插入时会出现嵌套内层的id不会自动同步外层
        model = WashingSymbolCollection
        fields = (
            "id",
            "name",
            "account_id",
            "system",
            'created_at',
            'updated_at',
            "washing_symbols"
        )
        ```
