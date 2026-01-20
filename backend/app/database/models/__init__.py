import os
import importlib.util
import inspect

CLASSES = {}

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3] 
        file_path = os.path.join(os.path.dirname(__file__), filename)

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                CLASSES[name] = obj

__all__ = list(CLASSES.keys())
