import string
import random
import unittest
import re

def _add_testing_string_lengths(passed_function, to_replace=" var ", **lengths):
    searched_str = [m.start() for m in re.finditer(to_replace, passed_function)]
    if len(searched_str) != 1:
        raise "replace error. found variables != 1"

    samples = {}

    for key, value in lengths.items():

        new_func = passed_function
        samples[key] = new_func.replace(to_replace, str(value))

    return samples


def make_string_testset(type_dict, **kwargs):
    '''
    Return value will be a dict with keys correlating to the dict and kwargs keys.\n
    this is in the form of:\n
    <dict variable name>["<type dict key>_<kwarg length variable name>"]\n
    \n
    example: strings["UpperCase_Short"]
    '''


    if not kwargs:
        raise "Input error. requires at least on argument"
    strings = {}


    # lengths
    for string_type, string_cmd in type_dict.items():
        cmd = f'''type_dict["{string_type}"] = _add_testing_string_lengths("''.join({string_cmd} for _ in range( var ))"'''
        for length_name, length_value in kwargs.items():

            cmd += f", {length_name}={length_value}"
        cmd += ")"
        exec(cmd)
        
        exec(f"{string_type} = " + "{}")
        for length_name, length_value in kwargs.items():
            # print(f"strings['{string_type}_{length_name}'] = {type_dict[string_type][length_name]}" )
            exec(f"strings['{string_type}_{length_name}'] = {type_dict[string_type][length_name]}" )

    
    return strings

class SelfTest(unittest.TestCase):

    def test_1(self):
        lengths = [ 1, 10, 100]
        type_dict = {
            "lower": "random.choice(string.ascii_lowercase)"
            , "upper": "random.choice(string.ascii_uppercase)"
        }
        strings = make_string_testset(type_dict, short=lengths[0], long=lengths[1], super=lengths[2])

        assert len(strings["lower_short"]) == lengths[0]
        assert len(strings["upper_short"]) == lengths[0]
        assert len(strings["lower_long"]) == lengths[1]
        assert len(strings["upper_long"]) == lengths[1]
        assert len(strings["lower_super"]) == lengths[2]
        assert len(strings["upper_super"]) == lengths[2]




if __name__ == '__main__':
    unittest.main()