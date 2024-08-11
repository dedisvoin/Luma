from colorama import Fore

from src.analize import tokenizer, loader
from src.parse import parser
from src.parse import preprocessor
from src.core import tokens

from src.debug import debug
from src.debug import tokenizer as debug_tokenizer
from src.debug import parser as debug_parser
from src.debug import memory as debug_memory


class Compiler:
    def __init__(self, debuging: bool, file: str) -> None:
        self.debug_ = debuging
        self.file_ = file

        debug.set_debug_log(self.debug_)

        def print_tokens(tokens: list[tokens.Token]):
            for token in tokens:
                print(f' token: {Fore.YELLOW}{token.value:>30}{Fore.RESET}   |   pos: {str(token.position):>70}   |   name: {Fore.MAGENTA}{token.signature:>40}{Fore.RESET}')
        debug_tokenizer.debug_tokens_first_stage.out_funct = print_tokens
        debug_tokenizer.debug_tokens_second_stage.out_funct = print_tokens

        def print_ast_nodes(nodes: list):
            for node in nodes:
                print(f' name:  {Fore.YELLOW}{node.__class__.__name__:>40}{Fore.RESET}   |   args: {Fore.GREEN}{str(node.__dict__):>120}{Fore.RESET}')
        debug_parser.debug_parsed_ast.out_funct = print_ast_nodes

        def print_memory_objects(memory_objects: list):
            for memory_object in memory_objects:
                if memory_object.inited:
                    print(f' name:  {Fore.YELLOW}{memory_object.name:>20}{Fore.RESET}   |   value: {Fore.GREEN}{str(memory_object.value.get_value()):>10}{Fore.RESET}   |   inited: {Fore.MAGENTA}{str(memory_object.inited):>10}{Fore.RESET}   |   mutable: {Fore.LIGHTBLUE_EX}{str(memory_object.mutable):>10}{Fore.RESET}')
                else:
                    print(f' name:  {Fore.YELLOW}{memory_object.name:>20}{Fore.RESET}   |   value: {Fore.GREEN}{str(memory_object.value):>10}{Fore.RESET}   |   inited: {Fore.MAGENTA}{str(memory_object.inited):>10}{Fore.RESET}   |   mutable: {Fore.LIGHTBLUE_EX}{str(memory_object.mutable):>10}{Fore.RESET}')
        debug_memory.debug_memory_objects.out_funct = print_memory_objects
        

    def load(self):
        self.code_file_ = loader.LoadLumaFile(self.file_)
        self.tokenizer_ = tokenizer.Tokenizer()
        self.tokenizer_.file = self.code_file_
        self.parser_ = parser.Parser()
        self.parser_.debug = self.debug_
        self.parser_.file = self.code_file_
        
    
    def tokenize(self):
        self.tokenizer_.tokenize()
        debug_tokenizer.debug_tokens_first_stage(self.tokenizer_.basic_tokens)
        self.tokenizer_.convert_signatures()
        debug_tokenizer.debug_tokens_second_stage(self.tokenizer_.standert_tokens)
        self.parser_.code_tokens = self.tokenizer_.standert_tokens

    def preprocess(self):
        self.preprocessor_ = preprocessor.PreProcessor()
        self.preprocessor_.standart_tokens = self.tokenizer_.standert_tokens
        self.preprocessor_.file = self.code_file_
        self.preprocessor_.parse()
        self.preprocessor_.execute()

        self.tokenizer_ = tokenizer.Tokenizer()
        self.tokenizer_.file = self.preprocessor_.file
        
        self.tokenizer_.tokenize()
        debug_tokenizer.debug_tokens_first_stage(self.tokenizer_.basic_tokens)
        self.tokenizer_.convert_signatures()
        debug_tokenizer.debug_tokens_second_stage(self.tokenizer_.standert_tokens)
        self.parser_.code_tokens = self.tokenizer_.standert_tokens

        

        

    def parse(self):
        self.parser_.generate_ast()
        debug_parser.debug_parsed_ast(self.parser_.nodes)

    def execute(self):
        for node in self.parser_.nodes:
            node.exec()
        debug_memory.debug_memory_objects(self.parser_.run_time_memory.get())
        

if __name__ == '__main__':
    import os, sys
    args = sys.argv
    LC = Compiler(1, args[1])
    LC.load()
    LC.tokenize()
    LC.preprocess()
    LC.parse()
    LC.execute()