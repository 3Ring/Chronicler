import os

from project import defaults as d
from project.helpers import private_convert
from project.models import Users


def translate_jinja(
    model,
    flag: str,
    game_id: int,
    user_id: int = None,
    dm_id: int = None,
    template: str = "blueprint.html",
    target_users: dict = None,
    **kwarg,
):
    """takes html from chronicler and returns handles: if, elif, else

    jinja variables that this can translate:
                (`current_user.id`, `tutorial.id`, `game.dm_id`)
                and any sqlalchemy class variable attached to the flag arg.
                ex: if flag == "user" then it can translate user.id, user.email, etc...
                to add in additional variables use the `**kwarg`

    :param model: class instance you want to use for variable replacement
    :param flag: `str` name of the model
    :param game_id: `Games.id` ID of game
    :param user_id: `Users.id` ID of user submitting the socket
    :param dm_id: `Users.id` of dm
    :param template: `str` of html template file name (this is primarily to change for testing)
    :param target_users: `dict`[`str` identifier, `int` id of target]
                        this is used to create multiple sockets based on the same information.
                        so that it will display differently for different users.
                        ex: drafts, private.
    :param **kwarg: any other variables to be subbed in ex: `char_img = 123`

    :return `dict[dict[str, str]`: [`str` target_users identifier, `dict` [`str` section name, `str` completed html]
    """
    if not target_users:
        return run(
            model,
            flag,
            game_id,
            user_id=user_id,
            dm_id=dm_id,
            template=template,
            **kwarg,
        )

    sockets = {}
    for target, id_ in target_users.items():
        sockets[target] = run(
            model,
            flag,
            game_id,
            user_id=user_id,
            dm_id=dm_id,
            template=template,
            target_user=id_,
            **kwarg,
        )
    return sockets


def run(
    model,
    flag: str,
    game_id: int,
    user_id: int = None,
    dm_id: int = None,
    target_user: int = None,
    template: str = "test.html",
    **kwarg,
):
    """creates socket for target_user"""

    set_globals(flag, user_id, dm_id, target_user)
    html_list = build_notes_template(template)

    raw_sections = find_sections_to_translate(html_list)
    finished = {}
    for name, section in raw_sections.items():
        finished[name] = finalize(section, model, game_id, **kwarg)
    return finished


def set_globals(flag, user_id, dm_id, target_user):
    """declare global variables"""
    global if_statements
    if_statements = 0
    global tutorial_id
    tutorial_id = Users.get_admin().id
    global _user_id
    _user_id = user_id
    global _dm_id
    _dm_id = dm_id
    global _flag
    _flag = flag
    global _target_user
    _target_user = target_user
    return


def get_socket_arg(line, start, end):
    """returns interior of string when start matched line prefix"""
    if line[: len(start)] == start:
        return line[len(start) : (len(end) * -1)]


def build_notes_template(filename: str):
    """gets and compiles html template

    this will only work in notes.html but can be easily changed for another page if needed

    :param filename: file name is the filename in the notes directory of templates ex: "blueprint.html"
    """
    raw_html = build_notes_template_get(filename)
    cleaned_list = build_notes_template_clean(raw_html)
    new_list = build_notes_template_read(cleaned_list)
    return new_list


def build_notes_template_clean(html):
    """takes raw html and jinja and converts it into a list. Removing trailing and ending whitespace"""
    file_list = html.split("\n")
    cleaned = []

    for line in file_list:
        stripped = line.strip()
        if stripped == "" or stripped == " ":
            pass
        else:
            cleaned.append(stripped)
    return cleaned


def build_notes_template_get(filename: str):
    """finds and opens the jinja template"""

    templates_path = "templates/notes"
    root_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(root_dir, templates_path)
    src = os.path.join(templates_dir, filename)
    return open(src).read()


def build_notes_template_read(html_list: list):
    """read page and find the "include" jinja links"""

    for i, line in enumerate(html_list):

        path = get_socket_arg(line, "{% include 'notes/", "' %}")
        if path:
            next_html = build_notes_template(path)
            list_1 = html_list[:i]
            list_2 = html_list[i + 1 :]
            final_list = list_1 + next_html + list_2

            return build_notes_template_read(final_list)
    return html_list


def find_sections_to_translate(html_list: list) -> list:
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
        hook = "{# translate_hook " + _flag + " #}"
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
        hook = "{# end_translate_hook " + _flag + " #}"
        found = line.find(hook)
        if found != -1:
            return i
    raise BaseException("socket flag not found")


def check_ignore(line):
    """logic to omit ignored sections

    this works with the Jinja comment flags `{# socket_ignore <flag> #}` and `{# endignore <flag> #}`
    """
    global ignore
    if ignore:
        if line == "{# endignore " + _flag + " #}":
            ignore = False
        return True
    else:
        if line == "{# socket_ignore " + _flag + " #}":
            ignore = True
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


def name_and_start_new_section(name):
    """name new list in socket"""
    global sections
    global section_name
    section_name = name
    sections[section_name] = []
    return


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


def check_for_section_flag(line: str) -> bool:
    start = "{# translate_section"
    if line[: len(start)] == start:
        return True
    return False


def set_sections(html_list):
    """cuts out ignored sections and splits relevant areas into a list."""
    global ignore
    ignore = False
    global sections
    sections = {}
    global section_name
    section_name = False

    start = check_section_start(html_list[0])
    for line in html_list[start:]:
        if check_ignore(line):
            continue
        if check_new_section(line):
            continue
        sections[section_name].append(line)
    return sections


def _or(arg_list):
    new_list = []
    if "or" in arg_list:
        for i, arg in enumerate(arg_list):
            if arg == "or":
                new_list.append(arg_list[:i])
                return_lists = _or(arg_list[i + 1 :])
                for l in return_lists:
                    new_list.append(l)
                return new_list

    else:
        return [arg_list]


def _and(arg_list):
    new_list = []
    if "and" in arg_list:
        for i, arg in enumerate(arg_list):
            if arg == "and":
                new_list.append(arg_list[:i])
                return_lists = _and(arg_list[i + 1 :])
                for l in return_lists:
                    new_list.append(l)
                return new_list
    else:
        return [arg_list]


def _and_or(arg_list):

    if "or" in arg_list:
        or_lists = _or(arg_list)
        if "or" in or_lists:
            return_ors = _or(or_lists)
            for l in return_ors:
                or_lists.append(l)
        for i, or_arg_list in enumerate(or_lists):
            temp_list = []
            if "and" in or_arg_list:
                return_ands = _and(or_arg_list)
                for l in return_ands:
                    temp_list.append(l)
                or_lists[i] = temp_list
            # make sure every expression is in a container, even if solo
            else:
                or_lists[i] = [or_lists[i]]

        for and_group in or_lists:
            for i, expression in enumerate(and_group):
                if not _if(expression):
                    and_group[i] = False
                else:
                    and_group[i] = True

        for i, and_group in enumerate(or_lists):
            if False in and_group:
                or_lists[i] = False
            else:
                or_lists[i] = True

        if True in or_lists:
            return True
        else:
            return False

    else:
        and_lists = _and(arg_list)
        for i, l in enumerate(and_lists):
            if not _if(l):
                and_lists[i] = False
                break
            else:
                and_lists[i] = True
        if False in and_lists:
            return False
        else:
            return True


def _if(arg):
    a = arg
    # simple if statement
    # ex: "if varable:"
    # if "or" in a or "and" in a:
    #     return _and_or(a)

    if type(a) == list:

        if len(a) == 1:
            if a[0]:
                return True
            else:
                return False

        if len(a) == 3:
            # equal
            if a[1] == "==":
                if a[0] == a[2]:
                    return True
                else:
                    return False
            # not equal
            elif a[1] == "!=":
                if a[0] != a[2]:
                    return True
                else:
                    return False
            # less than
            elif a[1] == "<":
                if a[0] < a[2]:
                    return True
                else:
                    return False
            # greater than
            elif a[1] == ">":
                if a[0] > a[2]:
                    return True
                else:
                    return False
            # less than or equal to
            elif a[1] == "<=":
                if a[0] <= a[2]:
                    return True
                else:
                    return False
            # greater than or equal to
            elif a[1] == ">=":
                if a[0] >= a[2]:
                    return True
                else:
                    return False
        else:
            raise BaseException("invalid argument")

    else:
        if a:
            return True
        else:
            return False


def switch(arg_list):
    if len(arg_list) > 0:
        if arg_list[0] == "if" or arg_list[0] == "elif":
            arg_list.pop(0)
            if "and" in arg_list or "or" in arg_list:
                return _and_or(arg_list)
            else:
                return _if(arg_list)
    else:
        pass


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
            generic_list.append(_target_user)
        elif item == "tutorial.id":
            generic_list.append(tutorial_id)
        elif item == "game.dm_id":
            generic_list.append(_dm_id)
        elif item == "bugs_id":
            generic_list.append(d.GameBugs.id)
        elif item[: len(_flag)] == _flag:

            generic_str = getattr(model, item[len(_flag) + 1 :])

            generic_list.append(generic_str)
        else:
            generic_list.append(item)
    return generic_list


def convert_string_to_generic(line: str) -> str:
    # TODO check if model needs the "." now that the eval is gone
    """checks if sqlalchemy class name is in string and replaces it with 'model'

    this is done so the code doesn't have to be rewritten for every different class
    """

    if line.find(f" {_flag}.") != -1:
        return line.replace(f" {_flag}.", " model.")
    else:
        return line


def stringify_and_add_whiteSpace(string_list):
    space_added = ""
    for word in string_list:
        space_added += word + " "
    stripped = space_added.strip()
    return stripped


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
    if_statements += change
    return


def remove_jinja_comments(html):

    new = []
    for line in html:
        if line[:2] == "{#" or line == "" or line == " ":
            pass
        else:
            new.append(line)

    return new


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
            currentU_key = "{{ " + "current_user.id" " }}"
            gameID_key = "{{ " + "id" " }}"

            # replace jinja variables
            # if
            html[i] = html[i].replace(model_key, str(value))
            html[i] = html[i].replace(currentU_key, str(_target_user))
            html[i] = html[i].replace(gameID_key, str(game_id))
        for key2, value in additional_keys.items():
            arg_key = "{{ " + "model." + str(key2) + " }}"
            html[i] = html[i].replace(arg_key, str(getattr(model, str(key2))))

        i += 1

    return html


class SortHtml:
    def __init__(self, conditionals, html_list):
        self.conditionals = conditionals
        self.html_list = html_list
        self.key = 0
        self.depth = 0
        self.allowed_depth = 0
        self.gatekeeper = True
        self._elif = {}
        self.final = []

    def run(self):
        i = 0
        while 0 < len(self.html_list):

            while self.gatekeeper and 0 < len(self.html_list):
                i += 1
                self.gate_open()
                self.key += 1
            while not self.gatekeeper and 0 < len(self.html_list):
                i += 1
                self.gate_closed()
                self.key += 1
        return self.final

    def gate_open(self):

        if not self.key in self.conditionals.keys():

            self.add_line()
            return
        type_ = self.conditionals[self.key][0]
        if type_ == "endif":
            self.open_endif()
            return
        if type_ == "if":
            if switch(self.conditionals[self.key]):
                self.passed_if()
            else:
                self.open_failed_if()
            return
        if type_ == "elif":
            self.open_elif()
            return
        if type_ == "else":
            self.open_else()
            return

    def gate_closed(self):

        if not self.key in self.conditionals.keys():
            self.remove_line()
            return

        type_ = self.conditionals[self.key][0]
        if type_ == "endif":
            self.closed_endif()
            return
        if type_ == "if":
            self.closed_if()
            return
        if type_ == "elif":
            self.closed_elif()
            return
        if type_ == "else":
            self.closed_else()

    def add_line(self):
        self.final.append(self.html_list[0])
        self.remove_line()
        return

    def remove_line(self):
        self.html_list.pop(0)
        return

    def open_endif(self):
        if self.allowed_depth == self.depth or self.allowed_depth + 1 == self.depth:
            self._elif.pop(self.depth)
            self.allowed_depth += -1
        self.depth += -1
        self.remove_line()
        return

    def passed_if(self):
        self.allowed_depth += 1
        self.depth += 1
        self._elif[self.depth] = False
        self.remove_line()
        return

    def passed_elif(self):
        self.allowed_depth += 1
        self.gatekeeper = True
        self._elif[self.depth] = False
        self.remove_line()
        return

    def open_failed_if(self):

        self.depth += 1
        self._elif[self.depth] = True
        self.gatekeeper = False
        self.remove_line()
        return

    def open_elif(self):
        self.gatekeeper = False
        self.allowed_depth += -1
        self.remove_line()
        return

    def open_else(self):
        self.gatekeeper = False
        self._elif[self.depth] = True
        self.allowed_depth += -1
        self.remove_line()
        return

    def closed_endif(self):
        if self.allowed_depth == self.depth or self.allowed_depth + 1 == self.depth:
            self.gatekeeper = True
            self._elif.pop(self.depth)
            # self.allowed_depth += -1
        self.depth += -1
        self.remove_line()

        return

    def closed_if(self):
        self.depth += 1
        self.remove_line()
        self._elif[self.depth] = False
        return

    def closed_elif(self):
        if self.allowed_depth == self.depth - 1 and self._elif[self.depth]:
            # check to make sure no other ifs have been triggered in this nest
            if switch(self.conditionals[self.key]):
                self.passed_elif()
            else:
                self.closed_failed_elif()
        else:
            self.closed_failed_elif()
        return

    def closed_passed_elif(self):
        self.allowed_depth += 1
        self._elif[self.depth] = False
        self.gatekeeper = True
        self.remove_line()
        return

    def closed_failed_elif(self):
        self.remove_line()
        return

    def closed_passed_else(self):
        self.allowed_depth += 1
        self.gatekeeper = True
        self.remove_line()
        return

    def closed_failed_else(self):
        self.remove_line()
        return

    def closed_else(self):
        if self.allowed_depth == self.depth - 1 and self._elif[self.depth]:
            self.closed_passed_else()
        else:
            self.closed_failed_else()
        return


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

    if if_statements != 0:
        raise BaseException("nesting error. statements are not even")
    return commands
