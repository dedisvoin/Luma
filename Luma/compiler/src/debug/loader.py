from src.debug import debug

debug_file_load_succes = debug.DebugMessage(debug.DebugSignatures.MESSAGE_LOADER)
debug_file_load_succes.add_message('File loaded succesfully. '+ debug.DebugSignatures.YES)

debug_file_load_error = debug.DebugMessage(debug.DebugSignatures.MESSAGE_LOADER)
debug_file_load_error.add_message('File loaded error. '+ debug.DebugSignatures.NO)