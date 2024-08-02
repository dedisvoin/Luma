import os, sys
import time
from src.lexer import tokenizer
from src.runtime import parser
from src.debugs import debug_compiler
from src.core import luma_binared


class LumaCompiler:
    def __init__(self, debug: bool = False, gen_bin: bool = False) -> None:
        self.debug = debug
        self.tokenizer = tokenizer.Tokenizer()
        self.parser = parser.Parser(debug)
        self.gen_bin = gen_bin

    def load_from_file(self, file_name: str):
        debug_compiler.debug_file_loading(file_name)
        self.tokenizer.load_file(file_name)
        
    def compile(self):
        start_time = time.time()
        self.tokenizer.tokenize()
        if self.debug >= 2: self.tokenizer.debug_first_stage_tokens()
        if self.debug >= 1: debug_compiler.debug_tokenize(len(self.tokenizer.basic_tokens), time.time() - start_time)
        start_time = time.time()
        self.tokenizer.convert_signatures()
        if self.debug >= 2: self.tokenizer.debug_second_stage_tokens()
        if self.debug >= 1: debug_compiler.debug_signatures_converting(len(self.tokenizer.standert_tokens), time.time() - start_time)

        self.parser.load_tokens(self.tokenizer.standert_tokens, self.tokenizer.file_name)
        start_time = time.time()
        self.parser.parse()
        if self.debug >= 1: debug_compiler.debug_parsing_finished(len(self.parser.commands), time.time() - start_time)
        if self.debug >= 2: self.parser.debug_commands()

    def execute(self):
        if not self.gen_bin:
            self.parser.execute()
            
    def get_run_time_memory(self):
        ...

class ArgsWrapper:
    def __init__(self) -> None:
        self.args = sys.argv
        self.file_name = self.args[1]
        self.debug_level = self.get_arg('-dl', 0)
        self.create_bin_file = self.get_arg('-gen-bin', 0)

    def get_arg(self, name: str, standart: any):
        try:
            index = self.args.index(name)
            value = self.args[index + 1]
        except:
            return standart
        return int(value)


if __name__ == '__main__':
    arg_wrapper = ArgsWrapper()
    comp = LumaCompiler(arg_wrapper.debug_level, arg_wrapper.create_bin_file)
    comp.load_from_file(arg_wrapper.file_name)
    comp.compile()
    comp.execute()
    if arg_wrapper.create_bin_file:
        luma_binared.save_file_binare_file(comp.tokenizer.file_name, comp.parser)
