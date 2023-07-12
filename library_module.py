import deprecator


def replacement():
    return "new function result"


deprecator.register_name_change(old_name="previous_name", new_function=replacement)
