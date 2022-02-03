from project.helpers.translate_jinja import _globals
from project.helpers.translate_jinja.set_sections import set_sections

def prune_template(html_list: list) -> list:
    """finds relevant socket section(s)

    :param html_list: complied html in a list line by line

    :return sections: a list of lists to be converted.
                    if there is only one section it will return [[section]]
    """

    scoped_html_list = set_socket_scope(html_list)
    pruned_html = scoped_html_list[
        find_html_start(scoped_html_list) : find_html_end(scoped_html_list)
    ]

    return set_sections(pruned_html)


def set_socket_scope(html: list) -> list:
    """prunes all html except for those inside of the {# socket_scope #}"""

    scope_start = html.index("{# socket_scope start #}")
    scope_end = html.index("{# socket_scope end #}")
    return html[scope_start + 1 : scope_end]


def find_html_start(html_list: list) -> int:
    """finds the start of the relevant html

    :param html_list: scoped html list
    :return int: index of start of relevant html
    """

    for i, line in enumerate(html_list):
        hook = "{# translate_hook " + _globals._flag + " #}"
        found = line.find(hook)
        if found != -1:
            return i + 1
    raise BaseException("socket flag not found")


def find_html_end(html_list):
    """finds the end of the relevant html

    :param html_list: scoped html list
    :return int: index of end of relevant html
    """
    for i, line in enumerate(html_list):
        hook = "{# end_translate_hook " + _globals._flag + " #}"
        found = line.find(hook)
        if found != -1:
            return i
    raise BaseException("socket flag not found")

