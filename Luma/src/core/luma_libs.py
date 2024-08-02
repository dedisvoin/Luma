
import importlib.util
import sys
sys.path.extend('../')

def load_python_file(file_path: str):
    file_path = file_path.replace('\\','/')
    module = importlib.util.spec_from_file_location(file_path.split('/')[-1],file_path)
    module = module.loader.load_module()
    return module

def get_lib_name(path: str) -> str:
        return path.split('/')[-1] + '.'

