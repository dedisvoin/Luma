import sys
sys.path.extend('../')

from src.core import luma_functions
from src.core import luma_values

fs = luma_functions.LumaFunctionsSaver()

@luma_functions.LumaFun(fs, 'print', args_count_ignore=True)
def _(args: list[luma_values.ValueConstruct]):
    value_args = []
    for arg in args:
        value_args.append(arg.value.value)
    print(*value_args)

@luma_functions.LumaFun(fs, 'println', args_count_ignore=True)
def _(args: list[luma_values.ValueConstruct]):
    value_args = []
    for arg in args:
        value_args.append(arg.value.value)
    print(*value_args, end='')

@luma_functions.LumaFun(fs, 'input', True)
def _(arg: luma_values.ValueConstruct):
    return luma_values.StringValue.Create(
        input(arg.value.value)
    )

@luma_functions.LumaFun(fs, 'len', True)
def _(arg: luma_values.ValueConstruct):
    if arg.value.type.name == 'String':
        return luma_values.IntValue.Create(
            len(arg.value.value)
        )
    
@luma_functions.LumaFun(fs, 'str', True)
def _(arg: luma_values.ValueConstruct):
        return luma_values.StringValue.Create(
            str(arg.value.value)
        )