import deprecator


def foo():
    return "foo"



def bar(*args, **kwargs):  # 'foo' used to be 'bar'
    return foo(*args, **kwargs)


deprecator.register_name_change(old_name=bar.__name__, new_name=foo.__name__)