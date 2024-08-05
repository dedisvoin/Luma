import sys
sys.path.extend('../')
import random

from src.core import luma_functions
from src.core import luma_values

fs = luma_functions.LumaFunctionsSaver()


@luma_functions.LumaFun(fs, 'random', True)
def _():
    return luma_values.FloatValue.Create(
        random.random()
    )

@luma_functions.LumaFun(fs, 'randint', True)
def _(start, stop):
    return luma_values.IntValue.Create(
        random.randint(start.value.value, stop.value.value)
    )

@luma_functions.LumaFun(fs, 'seed')
def _(seed):
    
    random.seed(seed[0].value.value)
    