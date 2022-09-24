def foo():
    return "foo"


def bar(*args, **kwargs):  # 'foo' used to be 'bar'
    return foo(*args, **kwargs)
