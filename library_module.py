import deprecator


def new_function():
    return "foo"


def deprecated_function(*args, **kwargs):  # 'foo' used to be 'bar'
    return new_function(*args, **kwargs)


deprecator.register_name_change(old_name="deprecated_function", new_function=new_function)
