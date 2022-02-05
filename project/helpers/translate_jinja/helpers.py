class Helpers:
    def get_socket_arg(self, line: str, start: str, end: str) -> str:
        """
        This is a function built to find the substring (inner variable) inside of jinja flag comments/include statements

        Given a string `line`, return the substring between `start` and `end`

        :param line: The string to be parsed.
        :param start: The start of the string to be cut
        :param end: The end of the string to be cut
        :return: The substring (socket argument).
        """
        if line[: len(start)] == start:
            return line[len(start) : (len(end) * -1)].strip()
        return False
