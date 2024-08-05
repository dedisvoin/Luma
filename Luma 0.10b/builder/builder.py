import os, sys
import shutil
import time

class CompilerObject:
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        
        self.code = f'''
code = \'''
{''.join(open(self.__file_name, 'r').readlines())}
\'''
import sys
sys.path.extend('../')
import luma
file_name = '{self.__file_name}'
interpretator = luma.LumaInterpretator(0, True)
interpretator.tokenizer.file_name = file_name
interpretator.load_from_code(code, file_name)
interpretator.compile()
interpretator.execute()
'''
        
    def start_compile(self):
        try:
            os.mkdir('./build')
            print('Build directory created!')
        except:
            
            shutil.rmtree('./build')
            time.sleep(1)
            os.mkdir('./build')
            print('Build directory recreated!')

        dummy_python_file_name = './build/'+self.__file_name.split('.')[0]+'.py'
        file = open(dummy_python_file_name, 'w')
        file.write(self.code)
        os.system('pip install pyinstaller')
        print(f'Luma code rewrited in python for dir {dummy_python_file_name}')
        os.system(f'pyinstaller "{dummy_python_file_name}" -D -F')



LMC = CompilerObject('main.lm')
LMC.start_compile()