import yaml

def constructor(loader, node) :
    fields = loader.construct_mapping(node)
    return Test(**fields)


yaml.add_constructor('!Test', constructor)

class Test(object) :
    def __init__(self, foo, bar=3) :
        self.foo = foo
        self.bar = bar
    def __repr__(self):
        return "%s(foo=%r, bar=%r)" % (self.__class__.__name__, self.foo, self.bar)


with open("../data/plants.yaml", "r") as fp:
    y = yaml.load(fp, Loader=yaml.SafeLoader)
    print(y)
