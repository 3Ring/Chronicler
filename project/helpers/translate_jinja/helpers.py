

def get_socket_arg(line: str, start: str, end: str) -> str:
    """
    This is a function built to find the substring (inner variable) inside of jinja flag comments/include statements

    Given a string `line`, return the substring between `start` and `end`

    :param line: The string to be parsed.
    :param start: The start of the string to be cut
    :param end: The end of the string to be cut
    :return: The substring (socket argument).
    """
    if line[: len(start)] == start:
        return line[len(start) : (len(end) * -1)]
    return False

def remove_jinja_comments(html):

    new = []
    for line in html:
        if line[:2] == "{#" or line == "" or line == " ":
            pass
        else:
            new.append(line)

    return new

def stringify_and_add_whiteSpace(string_list):
    space_added = ""
    for word in string_list:
        space_added += word + " "
    stripped = space_added.strip()
    return stripped
    