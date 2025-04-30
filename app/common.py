from fuzzywuzzy import fuzz

def str_compare(base_string:str ,string_to_compare:str, index:int)-> bool:
    return fuzz.ratio(base_string, string_to_compare) > index
