import builtins
import warnings

DEPRECATED_TO_NEW_NAME = {"bar": "foo", "baz": "qux"}

modified = False


def modify_imports():
    global modified
    if modified:
        return

    old_imp = builtins.__import__

    def custom_import(*args, **kwargs):
        module = old_imp(*args, **kwargs)
        # fromlist is fourth arg if given
        if len(args) >= 4 and isinstance(args[3], tuple):
            deprecated_imports = set(args[3]) & set(
                DEPRECATED_TO_NEW_NAME.keys()
            )
        else:
            deprecated_imports = {}

        for deprecated_import in deprecated_imports:
            warnings.warn(
                f"{deprecated_import} has been renamed!!! ; use 'from <location> import  {DEPRECATED_TO_NEW_NAME[deprecated_import]}' instead",
                category=DeprecationWarning,
                stacklevel=2
            )
        return module

    builtins.__import__ = custom_import
    modified = True
