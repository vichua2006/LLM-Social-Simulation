import json


def deserialize_first_json_object(json_string):
    start_bracket_index = json_string.index('{')
    end_bracket_index = get_corresponding_end_bracket_index(json_string, start_bracket_index)

    if start_bracket_index == -1 or end_bracket_index == -1 or start_bracket_index >= end_bracket_index:
        print("No valid JSON object found in the string.")
        return None

    
    json_string = json_string[start_bracket_index:end_bracket_index + 1]
    try: 
        return json.loads(json_string)
    except Exception as e:
        print("erroc when deserialize_first_json_object")
        print("original string: ", json_string)
        print(f'Error:{e}')

def get_corresponding_end_bracket_index(json_str, start_bracket_index):
    open_brackets = 0
    in_string = False

    for i in range(start_bracket_index, len(json_str)):
        current_char = json_str[i]

        if current_char == '"' and (i == 0 or json_str[i - 1] != '\\'):
            in_string = not in_string
        if not in_string:
            if current_char == '{':
                open_brackets += 1
            elif current_char == '}':
                open_brackets -= 1
                if open_brackets == 0:
                    return i
    # If the function reaches this point, it means there's no corresponding end bracket.
    return -1

def str_to_bool(s:str):
    return True if s.lower() == 'true' else False
