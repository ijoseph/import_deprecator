import deprecator


def foo():
    return "foo"


deprecator.register_name_change(old_name="bar", new_name="foo")


def bar(*args, **kwargs):  # 'foo' used to be 'bar'
    return foo(*args, **kwargs)
