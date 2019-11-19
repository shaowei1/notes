from marshmallow import fields, Schema, post_dump, pre_dump, pre_load, post_load

import datetime as dt


class MyDate(fields.Date):
    default_error_messages = {"invalid": "Please provide a valid date."}


class User:
    def __init__(self, name, email, income=1, debt=1):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.income = income
        self.debt = debt

    def __repr__(self):
        return f"<User(name={self.name!r})>"


class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author


class TitleCased(fields.Field):
    """Field that serializes to a title case string and deserializes
    to a lower case string.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        # dump
        # print("serialize", self, value, attr, obj)
        # attr: attribute, obj: User object
        if value is None:
            return ""
        # return value.title()
        # return value.lower()
        return value.upper()

    def _deserialize(self, value, attr, data, **kwargs):
        # load
        # print("deserialize", self, value, attr, data)
        return value.lower()


class UserSchema(Schema):
    slug = fields.Str()

    @pre_load
    def slugify_name(self, in_data, **kwargs):
        in_data["slug"] = in_data["slug"].lower().strip().replace(" ", "-")
        return in_data


    # name = fields.String(dump_only=True)
    name = fields.String(required=True, error_messages={"required": "Please provide a name."}
                         )
    # Function fields optionally receive context argument
    blog = fields.Function(lambda user, context: context["blog"] if user.name == "Freddie Mercury" else None)
    likes_bikes = fields.Method("writes_about_bikes")

    email = fields.String()
    created_at = fields.DateTime()
    titlename = TitleCased(attribute="name")

    since_created = fields.Method("get_days_since_created")

    def get_days_since_created(self, obj):
        return dt.datetime.now().day - obj.created_at.day

    # class Meta:
    # exclude = ("name",)
    # fields = ("name", "is_author", "likes_bikes", "blog")

    def writes_about_bikes(self, user):
        return "bicycle" in self.context["blog"].title.lower()

    # `Method` takes a method name (str), Function takes a callable
    balance = fields.Method("get_balance", deserialize="load_balance")

    income = fields.Integer()
    debt = fields.Integer()

    def get_balance(self, obj):
        return obj.income - obj.debt

    def load_balance(self, value):
        return float(value)

    @post_dump
    def f(self, data, *args, **kwargs):
        # print(self)
        # print(self.context)
        return data


user = User("Freddie Mercury", "fred@queen.com")
print(user, "\n")
blog = Blog("Bicycle Blog", author=user)
# schema = UserSchema(context={"blog": blog}, exclude=(("name",)))
# schema = UserSchema(context={"blog": blog}, )
schema = UserSchema()

# schema.context = {"blog": blog}
# result = schema.dump(user)
# result["is_author"]  # => True
# result["likes_bikes"]  # => True

# result = schema.load({"balance": "100.00"})


result = schema.load({"name": "Steve", "slug": "Steve Loria "})

print(result)
