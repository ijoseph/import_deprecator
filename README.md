# rename_deprecate
Warn end-user importing a specific function from a module at import time that its name is deprecated.

It's discouraged to modify `builtins.__import__`, but I can't see a better way to do it now. [(Need to check this out, though)](https://github.com/python/cpython/blob/2b428a1faed88f148ede131e3b86ab6227c6c3f0/Lib/importlib/_bootstrap.py#L1211) 

# Example
```bash
❯ python end_user.py
```
> ```
> end_user.py:6: DeprecationWarning: bar has been renamed!!! ; use 'from <location> import  foo' instead
>  from library_module import bar
>```  
