def switch(arg_list: list) -> bool:
    """if/elif/else logic (the nesting logic is handed by nested_conditional)
    :param arg_list: The list of simplified arguments that are being passed to the function
    :return: The result of the if statement.
    """
    if arg_list[0] == "if" or arg_list[0] == "elif":
        arg_list.pop(0)
        for o in _or(arg_list):
            if o:
                return o
        return False

def _or(arg_list: list) -> bool:
    """
    Given a list of strings, return a generator that yields the result of calling _and on all of the
    substrings separated by "or"

    :param arg_list: the simplified conditional list
    """

    j = 0
    for i, arg in enumerate(arg_list):
        if arg == "or":
            yield _and(arg_list[j:i])
            j = i + 1
    yield _and(arg_list[j:])


def _and(arg_list: list) -> bool:
    """
    checks each sub string separated by "and". if it finds one to be False it returns False.
    If all pass it returns True

    :param arg_list: the simplified conditional list with all "or" items removed
    :return: True or False
    """

    j = 0
    for i, arg in enumerate(arg_list):
        if arg == "and":
            if not _if(arg_list[j:i]):
                return False
            j = i + 1
    return _if(arg_list[j:])


def _if(arg) -> bool:
    """
    checks the simplified argument and returns its boolean value
    :param arg: The argument to be evaluated
    :return: A boolean value.
    """
    if type(arg) is list:
        if len(arg) == 1:
            return bool(arg[0])
        elif len(arg) == 3:
            if arg[1] == "==":
                return arg[0] == arg[2]
            elif arg[1] == "!=":
                return arg[0] != arg[2]
            elif arg[1] == "<":
                return arg[0] < arg[2]
            elif arg[1] == ">":
                return arg[0] > arg[2]
            elif arg[1] == "<=":
                return arg[0] <= arg[2]
            elif arg[1] == ">=":
                return arg[0] >= arg[2]
        else:
            raise BaseException("invalid argument")
    return bool(arg)
