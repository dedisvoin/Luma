import pickle



def save_file_binare_file(path: str, compiler):
    with open(path.split('.')[:-1][0]+'.lm.comp', 'wb') as file:
        pickle.dump(compiler, file)

def load_compiler_file(path: str):
    with open(path, 'rb') as file:
        return pickle.load(file)