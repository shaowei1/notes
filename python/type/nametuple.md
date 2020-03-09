
Product = namedtuple('Product', ['brand_id', 'brand_name'])


def test1():
    p = Product(brand_id=1, brand_name='22')
    print(p)
    d = Product._make([1, 3])
    print(d)
    print(p._replace(brand_name='ddd'))
    print(p._asdict())
    print(p._fields)
    """
    >>> p._fields            # view the field names
    ('x', 'y')

    >>> Color = namedtuple('Color', 'red green blue')
    >>> Pixel = namedtuple('Pixel', Point._fields + Color._fields)
    >>> Pixel(11, 22, 128, 255, 0)
    Pixel(x=11, y=22, red=128, green=255, blue=0)

    >>> Account = namedtuple('Account', ['type', 'balance'], defaults=[0]) #只能用于创建实例赋值
    >>> Account._field_defaults
    {'balance': 0}
    >>> Account('premium')
    Account(type='premium', balance=0)

    d = {'x': 11, 'y': 22}
    Point(**d)
    Point(x=11, y=22)
    """


EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade', defaults=[None, None, None, None, None])
print(EmployeeRecord(1, ))
for emp in map(EmployeeRecord._make, [{'name': 'shaowei', 'title': 'python',
                                       'age': 22, 'department': 'technology',
                                       'paygrade': None
                                       }.values()]):
    print(emp.name, emp.title)
for emp in map(Product._make, [(1, 2)]):
    print(emp.brand_id, emp.brand_name)

print(EmployeeRecord(**{'name': 'shaowei', 'title': 'python',
                        'age': 22, 'department': 'technology',
                        # 'paygrade': None
                        }))
