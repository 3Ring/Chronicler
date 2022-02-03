from project.helpers.translate_jinja.helpers import get_socket_arg
from project.helpers.translate_jinja import _globals

def set_sections(html_list):
    """cuts out ignored sections and splits relevant areas into a list."""
    # global ignore
    # ignore = False
    # global sections
    # sections = {}
    # global section_name
    # section_name = False

    start = check_section_start(html_list[0])
    for line in html_list[start:]:
        if check_ignore(line):
            continue
        if check_new_section(line):
            continue
        _globals.sections[section_name].append(line)
    return _globals.sections


def check_section_start(line):
    """checks if the first line of the html list is a section flag and returns the index to start the for loop"""
    global section_name
    section_name = get_socket_arg(line, "{# translate_section ", " #}")
    if not section_name:
        section_name = "no_sections"
        start = 0
    else:
        start = 1
    name_and_start_new_section(section_name)
    return start


def check_ignore(line):
    """logic to omit ignored sections

    this works with the Jinja comment flags `{# socket_ignore <flag> #}` and `{# endignore <flag> #}`
    """
    # global ignore
    if _globals.ignore:
        if line == "{# endignore " + _globals._flag + " #}":
            _globals.ignore = False
        return True
    else:
        if line == "{# socket_ignore " + _globals._flag + " #}":
            _globals.ignore = True
            return True
        return False


def check_new_section(line):
    """check if a new section is flagged

    this works with the Jinja comment flags {# translate_section <flag> <section_name>#} and {# endsection <flag> #}
    """
    found_flag = check_for_section_flag(line)
    if not found_flag:
        return False
    if found_flag:
        new_name = get_socket_arg(line, "{# translate_section ", " #}")
        name_and_start_new_section(new_name)
        return True


def check_for_section_flag(line: str) -> bool:
    start = "{# translate_section"
    if line[: len(start)] == start:
        return True
    return False


def name_and_start_new_section(name):
    """name new list in socket"""
    global sections
    global section_name
    section_name = name
    _globals.sections[section_name] = []
