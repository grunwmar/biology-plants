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
    dct = yaml.load(open(filename, "rb"), Loader=get_loader())
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

        return iterable

    recursion(dct)
    return grp, tml[0], len(lst)


def print_by_tags(filename, tags: list=None):
    grps, tml, count = parse(filename)

    string = "# Tags\n\n"

    for grp, items in dict(sorted(grps.items())).items():
        if  tags is None or grp in tags:
            string += f" - **{grp.lower()}:** "
            string += f"{", ".join([f"*{item}*" for item in items])}"
            string += "\n\n"

    string += f"\ntotal: {count}"

    with open("./tags.md", "w") as f:
        f.write(string)



if __name__ == "__main__":
    print_by_tags("../data/plants.yaml")
