import yaml
from dataclasses import dataclass


def test_constructor(loader, node):
    node = loader.construct_scalar(node)
    return f"!%plant::{node}"


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!plant", test_constructor)
    return loader


def load(filename):
    dct = yaml.load(open("plants.yaml", "rb"), Loader=get_loader())
    return dct


def parse(filename):
    dct = load(filename)
    lst = list()
    grp = dict()

    tml = [0]

    @dataclass
    class Species:
        name: str = None
        tags: list = None

        def __str__(self):
            tags = ",".join([f"{i}" for i in self.tags])
            return f"[{self.name} > {tags}]"

        def __repr__(self):
            return str(self)

    def recursion(iterable):
        if isinstance(iterable, list):
            for item in iterable:
                recursion(item)

        elif isinstance(iterable, dict):
            for key, item in iterable.items():
                if key.startswith("!%plant::"):
                    name = key.replace("!%plant::", "")
                    spec = Species(name=name, tags=item)
                    lst.append(spec)
                    for tag in spec.tags:

                        if len(tag) > tml[0]:
                            tml[0] = len(tag)

                        try:
                            grp[tag] += [name]
                        except KeyError:
                            grp[tag] = [name]

                else:
                    recursion(item)
        else:
            ...

        return iterable

    r = recursion(dct)
    return grp, tml[0], len(lst)


def print_by_tags(filename):
    grps, tml, count = parse(filename)
    for grp, items in grps.items():
        ldif = tml - len(grp)
        print(f">\033[1;4m {grp:<{tml}} \033[0m")
        for item in items:
            print(f"       + \033[92m{item}\033[0m")
        print("")

    print("\n total:", count)



if __name__ == "__main__":
    print_by_tags("plants.yaml")
