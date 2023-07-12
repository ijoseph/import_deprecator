import deprecator


def new_function():
    return "new function result"


deprecator.register_name_change(old_name="deprecated_function", new_function=new_function)
