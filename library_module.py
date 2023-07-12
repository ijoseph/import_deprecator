import deprecator


def replacement():
    return "new function result"


deprecator.register_name_change(old_name="deprecated", new_function=replacement)
