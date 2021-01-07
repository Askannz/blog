Title: Importing from a parent or sibling folder in Python
Date: 2021-01-07 22:44
Category: Python
Tags: python, modules, subfolders, import

# The problem

Suppose that you have a script `script.py` that imports something from another file `dependency.py`. The two files are at the same level in the project hierarchy.

```
my_project/
├── script.py
└── dependency.py
```

To import whatever you need from `dependency.py`, you can just use an absolute import statement, like so:

```
from dependency import my_function
```

So far so good. But now let's imagine the project has grown a bit and you need to put `script.py` into a subfolder, whereas `dependency.py` needs to stay at the top-level because other files depend on it.

```
my_project/
├── subfolder
│   └── script.py
└── dependency.py
```

If you try to run the script from the root folder, you'll be greeted with this:

```
$ python subfolder/script.py
Traceback (most recent call last):
  File "/home/robin/tmp/python_module_demo/my_project/subfolder/script.py", line 1, in <module>
    from dependency import my_function
ModuleNotFoundError: No module named 'dependency
```

Ok, Python cannot find the `dependency` module anymore. Maybe we need to tell it to fetch it one folder higher ? Let's try changing `from dependency import my_function` to `from ..dependency import my_function`.

```
$ python subfolder/script.py
Traceback (most recent call last):
  File "/home/robin/tmp/python_module_demo/my_project/subfolder/script.py", line 1, in <module>
    from ..dependency import my_function
ImportError: attempted relative import with no known parent package
```

Still doesn't work, but the error is different. You can try running `script.py` from `subfolder/` instead, but you'll get similar errors.


# The solution

Every Python programmer has been confronted to that issue. Curiously, trying to Google "python import from parent folder" will almost always point you toward weird hacks that involve modifying `sys.path`, setting a `PYTHONPATH` variable, or even using pip to link the current directory as a development package. There is a much more idiomatic and (in my opinion) much more practical solution.

Simply put all your code in a subfolder (which we'll call `my_module` because that's actually what it is), like so:

```
my_project/
└ my_module
  ├── subfolder
  │   └── script.py
  └── dependency.py
```

For the import statement, use `from ..dependency import my_function`. The `..` means "one level higher from `subfolder`, which correspond to `my_module`.

So how are you supposed to run `script.py` now ? **The trick is to tell Python not to run it as a script, but as a Python module.** You can do this using the `-m` parameter, like so:

```
python -m my_module.subfolder.script
```

Now, because all the code is encapsulated inside a single module, Python will have no issue fetching `my_function` from one file up. Note that the working directory is still the one where you invoke the command from, so `my_project/` in this case.

This solution also solves the problem of imports from sibling folders. Let's say for example that you have the following project structure:

```
my_project/
├── subfolder_A
│   └── script_A.py
└── subfolder_B
    └── dependency_B.py
```

Where `script_A.py` wants to import `my_function` from `dependency_B.py`. Just put everything in a Python module like before:

```
my_project/
└ my_module
  ├── subfolder_A
  │   └── script_A.py
  └── subfolder_B
      └── dependency_B.py
```

Now `script_A.py` can import the function like this: `from ..subfolder_B.dependency_B import my_function`, and you can run it with

```
python -m my_module.subfolder_A.script_A
```

# Additional tricks

## The __main__ guard

In both the examples above, our target script is also itself a module, and therefore it's possible to import stuff from it. However, when a module is imported, everything in its global scope is executed, which can have unintende consequences. In other words, if your `script.py` looks like this:

```
def my_other_function():
    print("Hello from my_other_function")
    
print("Hello")
```

Then importing `from script import my_other_function` in another file will also execute the `print("Hello")` statement.
This is why Python script traditionally wrap their code in a `if __name__ == "__main__":` statement:

```
def my_other_function():
    print("Hello from my_other_function")
    
if __name__ == "__main__":
    print("Hello")
```

This way, `print("Hello")` will only execute if the module is ran directly with `python -m`, and not if `script` is imported by some other module.


## Run a whole folder as a script

This is a small but neat feature. In the first example above, if you rename `script.py` as `__main__.py`, you will be able to call `subfolder` directly as if it was an executable script itself: `python -m my_module.subfolder`. It can be pretty useful to get rid of superflous submodules and shorten the invocation path.

That's it, I hope this blog post was useful to you. I wrote it after being frustrated at the module system of Python for so long, and realizing that the solution was much simpler that what Google would suggest.
