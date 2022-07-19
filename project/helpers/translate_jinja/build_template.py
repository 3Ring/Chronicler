import os

from project.helpers.translate_jinja.init import Init
from project.helpers.translate_jinja.helpers import Helpers


class Build(Init, Helpers):
    def build_template(self, filename: str) -> list:
        """
        Opens Jinja template `filename` and parses it into a list of non-empty strings of html/jinja

        :param filename: the name of the jinja file to parse ex: "blueprint.html"
        :return: A list of dictionaries. Each dictionary is a note.
        """

        raw_html = self.get(filename)
        cleaned_list = self.clean(raw_html)
        new_list = self.read(cleaned_list)
        return new_list

    def clean(self, html: str) -> list:
        """
        Given a string of html, return a list of the lines striped of whitespace that are not empty

        :param html: The HTML string to be cleaned
        :return: a list of non-empty strings of html/jinja.
        """
        cleaned = []
        for line in html.split("\n"):
            if len(line.strip()) != 0:
                cleaned.append(line.strip())
        return cleaned

    def get(self, filename: str) -> str:
        """
        Reads a file from the templates/notes directory and returns the contents as a string

        :param filename: The name of the jinja template file to be used
        :return: the file as a string.
        """
        from flask import current_app

        src = os.path.join(
            current_app.root_path, current_app.template_folder, "notes", filename
        )
        return open(src).read()

    def read(self, html_list: list) -> list:
        """
        Reads the html list and looks for the path of the included file.
        If found, it reads the included file and returns the included file's contents.
        If not found, it returns the original html file.

        :param html_list: list of html to search
        :return: a complete html list
        """

        for i, line in enumerate(html_list):
            path = self.get_socket_arg(line, "{% include 'notes/", "' %}")
            if path:
                return (
                    html_list[:i]
                    + self.build_template(path)
                    + self.read(html_list[i + 1 :])
                )
        return html_list

    def __init__(
        self,
        model,
        flag: str,
        game_id: int,
        user_id: int = None,
        dm_id: int = None,
        target_user: int = None,
        target_users: dict = None,
        template: str = "blueprint.html",
    ):
        super().__init__(
            model, flag, game_id, user_id, dm_id, target_user, target_users, template
        )
        self.html = self.build_template(template)
