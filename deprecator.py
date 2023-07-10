import builtins
import warnings

DEPRECATED_TO_NEW_NAME = {}

modified = False


def register_deprecation(old_name: str, new_name: str) -> None:
    """
    Register that function with name 'old_name' is now called 'new_name'
    """
    DEPRECATED_TO_NEW_NAME.update({old_name: new_name})
    _modify_imports()


def _modify_imports():
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
                    f"  Consider using \n    from {args[0]} import {DEPRECATED_TO_NEW_NAME[deprecated_import]}\n  instead of"
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
        return module

    builtins.__import__ = custom_import
    modified = True
