#!/usr/bin/env python3.10

import importlib.util
import sys


def run_module_check():
    modules = ['tkinter']

    for mod in modules:
        if mod in sys.modules:
            print(f"{mod!r} already in sys.modules")
        elif (spec := importlib.util.find_spec(mod)) is not None:
            module = importlib.util.module_from_spec(spec)
            sys.modules[mod] = module
            spec.loader.exec_module(module)
            print(f"{mod!r} has been imported")
        else:
            print(f"can't find the {mod!r} module")


def run_shortcut_creator():
    import os
    import platform
    from pyshortcuts import make_shortcut

    """
    if platform == "linux" or platform == "linux2":
        icon = os.path.relpath('logo.icns')
    elif platform == "darwin":
        icon = os.path.relpath('logo.icns')
    elif platform == "win32" or "win64":
        icon = os.path.relpath('logo.ico')
    """

    main_script = os.path.relpath("plate_map_converter.py")

    make_shortcut(main_script, name='Plate Map Converter', desktop=True)

run_module_check()
run_shortcut_creator()