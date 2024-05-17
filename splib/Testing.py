
def method(self, node, a, **kwargs):
    print(self)
    print(node)
    print(a)
    print(kwargs)


if __name__ == "__main__":
    dict = { "node" : 12, "self" : 1, "a" : "azd", "jnd" : 5 }
    a = method
    method(**dict)
    print(a.__name__)