import weakref

class A:
    instances = []
    value=0
    def __init__(self, name=None):
        # 
        self.__class__.instances.append(weakref.proxy(self))
        self.name = name
    def __str__(self):
        return self.name
    def filter(name=None,value=None):
        list=[]
        for loop in A.instances:
            try:
                name_loop=None
                value_loop=None
                if name == None:
                    name_loop = loop.name
                else: name_loop=name
                if value == None:
                    value_loop = loop.value
                else: value_loop=value
                if name_loop == loop.name and value_loop==loop.value:
                    list.append(loop)
            except:
                pass
        return list



a2 = A('a2')
a2.value=5
a6=A("a7")
a6.value=7

for instance in A.filter(value=5):
    try:
        print(instance)
    except:
        pass



