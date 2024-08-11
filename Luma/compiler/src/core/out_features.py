from src.core import luma_types, luma_values

def LumaListToPyList(array: list[luma_values.LumaValue]):
    out_array = []
    for value in array:
        if value.get_type() == luma_types.BaseLumaTypes.L_List:
            out_array.append(LumaListToPyList(value.get_value()))
        else:
            out_array.append(value.get_value())
    return out_array

def LumaListToOutList(array: list[luma_values.LumaValue]):
    out_array = []
    for value in array:
        if value.get_type() == luma_types.BaseLumaTypes.L_List:
            out_array.append(LumaListToPyList(value.get_out_value()))
        else:
            out_array.append(value.get_out_value())
    return out_array