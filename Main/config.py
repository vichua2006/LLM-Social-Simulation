''' A configuration file with LLM config and keys, to avoid circular imports'''

victor_opeai_key = "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"


AUTOGEN_LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-3.5-turbo",
            "api_key": victor_opeai_key,
        },  
    ], 
    "temperature": 0.0, # has been set to 0 from the very start of implementing conversation
    "top_p": 1, # 1 by default
}