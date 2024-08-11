from src.debug import debug

debug_memory_objects = debug.DebugMessage(debug.DebugSignatures.MESSAGE_MEMORY)
debug_memory_objects.add_message('Memory outed. '+ debug.DebugSignatures.YES)