# `import_deprecator`

This was motivated by the following issue:
in a large code base, it's common to use the `from some.long.chain.of.packages import some_function` [syntax](https://docs.python.org/3.10/reference/simple_stmts.html#import:~:text=from%20foo.bar%20import%20baz%20%20%20%20%23%20foo%2C%20foo.bar%2C%20and%20foo.bar.baz%20imported%2C%20foo.bar.baz%20bound%20as%20baz) to import `some_function`, as it's more ergonomic than imply importing `some.long.chain.of.packages` and using this whole string each time the function is called, and also more straightforward than using the `as` syntax to create an alias of the same. 

Developers/ maintainers of `some.long.chain.of.packages` might, of course, later want to refactor `some_function(...)` to be called `some_renamed_function`.

This presents an issue for the callers of `some_function`, who now must change all their imports (and calls) accordingly. 

One solution is to keep `some_function` around and simply redirect it to `some_renamed_function`, and use something like  [`Deprecated`](https://pypi.org/project/Deprecated/):

```python
# some/long/chain/of/packages.py
from deprecated import deprecated


def some_renamed_function(...):
    # do_busienss_logic

@deprecated(reason="Use some_renamed_function instead")
def some_function(*args, **kwargs):
    return some_renamed_function(*args, **kwargs)
```

```python
>>> from some.long.chain.of.packages import some_function  # no warning
>>> # do other stuff
>>> some_function()  # warning appears only now

```

However, this will warn _at the time that `some_function` is called_, which is often far after the fact of importing it, and inconvenient for end-users to change, especially if the import is in a long Jupyter Notebook several screen-scrolls above where it is actually used. 

More convenient would be to warn the user as _soon as they import_ the deprecated name, as this will be close to where they'd need to change it.

This project achieves that:

```python
# some/long/chain/of/packages.py
import deprecator

def some_renamed_function(...):
    # do_busienss_logic

deprecator.register_name_change(old_name="some_function", new_function=some_renamed_function)
```

```python
>>> from some.long.chain.of.packages import some_function

  Object 'some.long.chain.of.packages.some_function' has been renamed to 'some.long.chain.of.packages.some_renamed_function'!
  Consider using
  from some.long.chain.of.packages.some_function import some_renamed_function
  instead of
  from some.long.chain.of.packages.some_function import some_function
```



## Notes

Modifying  `builtins.__import__` is discouraged, but I can't see a better way to do it now as `importlib` doesn't appear to handle `fromlist` imports. [(Need to check this out, though)](https://github.com/python/cpython/blob/2b428a1faed88f148ede131e3b86ab6227c6c3f0/Lib/importlib/_bootstrap.py#L1211) 


## Future Milestones
1. make into an installable
1. Use decorator syntax
2. Warn if overwriting existing deprecated function
6. Support moving (to a new module) without renaming
7. Verify support for arbitrary objects rather than just `typing.Callable`s
8. Verify support for multiple-argument from-list 
9. Handle version numbers


