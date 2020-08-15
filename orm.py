


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
        print("it's here")
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
    Email = StringField('email')
    password = StringField('password')
print('====================')
print(User.__dict__)
u = User(id='12345', name='Michael', Email='test@orm.org', password='my-pwd')
u.ceo = 'jack'
print(u.ceo)
u.save()



'''
为什么要把attr里面和Field相关的属性删掉呢

首先实例的属性会覆盖类的属性，但是因为我们user的类没有id这样的属性
class User下面的id的定义只是定义field，然后u = user（。。。）的时候是定义了dictionary，但是initialize object的paramter要和class的variable一样, 因为metaclass在define user的时候就生效了而不是到initilization的时候
这时候class User下面的variable name就已经插入到mapping里面，如果u = User（。。。）parameter不一样的话就会getattrt到None了

如果不删的话getattr会先去看u的__dict__然后没有，就会去call User的__dict__,然后拿到不对的。因为没有删
如果删掉的话两个__dict__都拿不到，就会去call default的__getattr__这时候就直接call dict[key]拿到对的value了

User的initialization是和dict一样，有[key]没有u.id
参考资料：https://www.cnblogs.com/ArsenalfanInECNU/p/9100874.html
'''
