from project.helpers.translate_jinja import _globals
from project.helpers.misc import private_convert
from project.setup_ import defaults as d

def set_conditionals(section: list, model):
    commands = {}
    for i, line in enumerate(section):
        conditional = get_jinja_conditional_list(line)
        if conditional:
            if_or_endif = check_for_start_or_end(conditional)
            if if_or_endif:
                update_if_statements(if_or_endif)
            generic_conditional = convert_conditional_to_generic(model, conditional)
            commands[i] = generic_conditional
    if _globals.if_statements != 0:
        raise BaseException("nesting error. statements are not even")
    return commands

def get_jinja_conditional_list(line: str):
    """checks if line is a conditional and returns it as a list if so

    :return `False`: if string is not a Jinja conditional
    :return `list`: if string is a Jinja conditional
    """
    if line[0:2] == "{%" and line[len(line) - 2 :] == "%}":
        word_list = []
        conditional = line[2:-2]
        conditional.strip()
        conditional_list = conditional.split(" ")

        for word in conditional_list:
            if word == " " or word == "":
                continue
            word = word.strip()
            word_list.append(word)
        return word_list
    return False

def check_for_start_or_end(conditional_list):
    """checks for beginning or end of conditional

    :return `Literal['if']`: if list is an "if" conditional
    :return `Literal['endif']`: if list is the end of a conditional
    """
    for item in conditional_list:
        if item == "endif" or item == "if":
            return item
    return False

def update_if_statements(condition):
    """updates global if_statements count"""
    global if_statements

    if condition == "endif":
        change = -1
    elif condition == "if":
        change = 1
    else:
        raise BaseException("not valid condition")
    _globals.if_statements += change
    return


def convert_conditional_to_generic(model, list_):
    """converts all variables to their values

    ex: (['if', 'current_user.id', '!=', 'game.dm_id'] becomes generic_list: ['if', 1, '!=', 3]

    :param model: model of the table the socket is being made for. ex: "Notes"
    :param list_: conditional words list
    """

    generic_list = []
    for item in list_:
        if item.lower() == "true" or item.lower() == "false":
            generic_list.append(private_convert(item))
        elif item == "current_user.id":
            generic_list.append(_globals._target_user)
        elif item == "tutorial.id":
            generic_list.append(_globals.tutorial_id)
        elif item == "game.dm_id":
            generic_list.append(_globals._dm_id)
        elif item == "bugs_id":
            generic_list.append(d.GameBugs.id)
        elif item[: len(_globals._flag)] == _globals._flag:

            generic_str = getattr(model, item[len(_globals._flag) + 1 :])

            generic_list.append(generic_str)
        else:
            generic_list.append(item)
    return generic_list
