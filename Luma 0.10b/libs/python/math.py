import sys
sys.path.extend('../')
import math

from src.core import luma_functions
from src.core import luma_values
from src.core import luma_types

fs = luma_functions.LumaFunctionsSaver()

@luma_functions.LumaFun(fs, 'sin', True, types=[[luma_types.LumaTypes.get('Float'), luma_types.LumaTypes.get('Int')]])
def _(arg: luma_values.ValueConstruct):
    return luma_values.FloatValue.Create(
        math.sin(arg.value.value)
    )

@luma_functions.LumaFun(fs, 'cos', True, types=[[luma_types.LumaTypes.get('Float'), luma_types.LumaTypes.get('Int')]])
def _(arg: luma_values.ValueConstruct):
    return luma_values.FloatValue.Create(
        math.cos(arg.value.value)
    )

@luma_functions.LumaFun(fs, 'radians', True, types=[[luma_types.LumaTypes.get('Float'), luma_types.LumaTypes.get('Int')]])
def _(arg: luma_values.ValueConstruct):
    return luma_values.FloatValue.Create(
        math.radians(arg.value.value)
    )

@luma_functions.LumaFun(fs, 'degrees', True, types=[[luma_types.LumaTypes.get('Float'), luma_types.LumaTypes.get('Int')]])
def _(arg: luma_values.ValueConstruct):
    return luma_values.FloatValue.Create(
        math.degrees(arg.value.value)
    )