import builtins
import sys
from typing import Callable
import warnings


DEPRECATED_TO_NEW_NAME = {}

modified = False


def register_name_change(old_name: str, new_function: Callable) -> None:
    """
    Register that function with name 'old_name' is now called 'new_name'.

    """
    DEPRECATED_TO_NEW_NAME.update({old_name: new_function.__name__})
    _patch_import()
    _patch_module(old_name, new_function)


def _patch_import():
    """
    Patch 'from <module> import <object>' calls
    """
    old_imp = builtins.__import__

    def custom_import(*args, **kwargs):
        module = old_imp(*args, **kwargs)
        # fromlist is fourth arg if given
        if len(args) >= 4 and isinstance(args[3], tuple):
            deprecated_imports = set(args[3]) & set(DEPRECATED_TO_NEW_NAME.keys())
        else:
            deprecated_imports = {}

        for deprecated_import in deprecated_imports:
            warnings.warn(
                (
                    f"\n  Object '{args[0]}.{deprecated_import}' has been renamed to "
                    f"'{args[0]}.{DEPRECATED_TO_NEW_NAME[deprecated_import]}'!\n"
                    f"  Consider using \n  'from {args[0]} import {DEPRECATED_TO_NEW_NAME[deprecated_import]}'\n  "
                    f"instead of"
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
        return module

    builtins.__import__ = custom_import
    modified = True


def _patch_module(old_name: str, new_function: Callable) -> None:
    """
    Create old_name as copy of new_function in the same module.
    """
    function_mod = new_function.__module__
    # TODO: warn if overwriting existing deprecated function
    setattr(sys.modules[function_mod], old_name, new_function)
