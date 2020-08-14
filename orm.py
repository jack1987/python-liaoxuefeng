


class Field():
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return f'{self.__class__.__name}:{self.name}'

class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, 'bigint')

class StringField(Field):
    def __init__(self, name):
        super().__init__(name, 'varchar(100)')

#need type class to be parent class
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        __mappings__ = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                __mappings__[key] = value
        for key in __mappings__.keys():
            del attrs[key]
        attrs['__mappings__'] = __mappings__
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)

#nedd dict and metaclass =
class Model(dict, metaclass = ModelMetaclass):
    def __init__(self, **kw):
        # this is for dictonary a=1,b=2
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object does has this key %s" %key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        table_name = self.__table__
        fields = []
        args = []
        for key, value in self.__mappings__.items():
            #key是data class的variable name
            #value是定义的Field的subclass
            fields.append(value.name) #在field class里面定义了这个name
            args.append(getattr(self, key, None))
        statement = 'Insert into table %s columns (%s) with value (%s)' %(table_name, ','.join(fields), ','.join(args))
        print(statement)


class User(Model):
    id = IntegerField('id')
    name = StringField('Username')
    email = StringField('email')
    password = StringField('password')

u = User(id='12345', name='Michael', email='test@orm.org', password='my-pwd')
u.ceo = 'jack'
print(u.test)
u.save()



'''
为什么要把attr里面和Field相关的属性删掉呢
首先实例的属性会覆盖类的属性，但是因为我们user的类没有id这样的属性
'''
