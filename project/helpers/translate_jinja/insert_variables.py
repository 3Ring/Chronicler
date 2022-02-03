from project.helpers.translate_jinja import _globals
from project.helpers.translate_jinja.set_conditionals import set_conditionals
from project.helpers.translate_jinja.sort_html import SortHtml
from project.helpers.translate_jinja.helpers import remove_jinja_comments, stringify_and_add_whiteSpace


def finalize(section: list, model, game_id: int, **kwarg):

    conditionals = set_conditionals(section, model)
    # generic_socket_list = None
    # if conditionals:
    program = SortHtml(conditionals, section)
    sorted_section = program.run()
    generic_socket_list = parse_html_list(sorted_section)
    final_socket_list = pass_model_variables(
        generic_socket_list, model, game_id, **kwarg
    )
    final_socket = stringify_and_add_whiteSpace(final_socket_list)
    return final_socket

def parse_html_list(html: list) -> list:
    """removes jinja comments and converts class names to 'model'"""
    htmlWithout_jinja_comments = remove_jinja_comments(html)
    parsed_list = []
    for line in htmlWithout_jinja_comments:
        parsed_list.append(convert_string_to_generic(line))
    return parsed_list


def pass_model_variables(html, model, game_id, **additional_keys):
    html = html
    columns = {}
    for column in model.__table__.columns:
        columns[str(column.key)] = getattr(model, str(column.key))

    # iterate through each key/value pair in the model instance's attributes
    i = 0
    while i < len(html):

        for key, value in columns.items():
            model_key = "{{ " + "model." + key + " }}"
            currentU_key = "{{ " + "current_user.id" + " }}"
            gameID_key = "{{ " + "id" + " }}"

            # replace jinja variables
            # if
            html[i] = html[i].replace(model_key, str(value))
            html[i] = html[i].replace(currentU_key, str(_globals._target_user))
            html[i] = html[i].replace(gameID_key, str(game_id))
        for key2, value in additional_keys.items():
            arg_key = "{{ " + "model." + str(key2) + " }}"
            html[i] = html[i].replace(arg_key, str(getattr(model, str(key2))))

        i += 1

    return html

def convert_string_to_generic(line: str) -> str:
    # TODO check if model needs the "." now that the eval is gone
    """checks if sqlalchemy class name is in string and replaces it with 'model'

    this is done so the code doesn't have to be rewritten for every different class
    """

    if line.find(f" {_globals._flag}.") != -1:
        return line.replace(f" {_globals._flag}.", " model.")
    else:
        return line