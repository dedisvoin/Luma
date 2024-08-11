from src.debug import debug


debug_tokens_first_stage = debug.DebugMessage(debug.DebugSignatures.MESSAGE_TOKENIZER)
debug_tokens_first_stage.add_message('First stage tokens outed. '+ debug.DebugSignatures.YES)


debug_tokens_second_stage = debug.DebugMessage(debug.DebugSignatures.MESSAGE_TOKENIZER)
debug_tokens_second_stage.add_message('Second stage tokens outed. '+ debug.DebugSignatures.YES)