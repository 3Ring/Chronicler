from project.setup import defaults as d
from project.helpers.misc import bool_convert


class Checks:
    def check_end(self) -> bool:
        """If the current line is the end of the hook, return True. Otherwise, return False"""
        if self.line == self.flag_hook_end:
            return True
        return False

    def checks(self) -> bool:
        """Check if the line is in scope should be added to the socket"""
        if not self.in_scope():
            return False
        if not self.nested_conditionals():
            return False
        if not self.comment_or_empty():
            return False
        return True

    def in_scope(self) -> bool:
        """
        Check if the current line is in scope

        :return: boolean that indicates whether the current line is within the scope of the current section.
        """
        if not self.scope_found:
            self.find_start()
            return False
        elif not self.hook_found:
            self.find_hook()
            return False
        elif self.ignore():
            return False
        self.check_new_section()
        return True

    def find_start(self):
        """If the current line is the start of the scope, set the scope_found flag to True"""
        if self.line == self.flag_scope:
            self.scope_found = True

    def find_hook(self):
        """If the line contains the flag_hook, then set the hook_found flag to True and set the section_name to
        the name of the section"""
        if self.line.find(self.flag_hook) != -1:
            self.hook_found = True
            name = self.get_socket_arg(self.line, self.flag_hook, " #}")
            self.set_section_name(name)

    def ignore(self) -> bool:
        """If the current line is in the ignore range, return True. Otherwise, return False"""
        if self._ignore:
            if self.line == self.flag_ignore_end:
                self._ignore = False
                return False
            return True
        if self.line == self.flag_ignore:
            self._ignore = True
            return True
        return False

    def top_checks(self):
        """checks to see if it's the start of a new section or new condition and follows up"""
        self.check_new_section()
        self.check_new_condition()

    def check_new_condition(self):
        """if a new condition is found, create and set a generic condition to be parsed by switch"""
        if self.line[:2] != "{%":
            self.condition.clear()
            self.con_type = None
            return
        con = [w.strip() for w in self.line[2:-2].strip().split(" ")]
        self.con_type = con[0]
        if len(con) == 1:
            self.condition = con
            return
        generic_list = [con[0]]
        for item in con[1:]:
            item = item.strip().lower()
            if item == "true" or item == "false":
                generic_list.append(bool_convert(item))
            elif item == "current_user.id":
                generic_list.append(self.target_user)
            elif item == "tutorial_id":
                generic_list.append(self.tutorial_id)
            elif item == "game.dm_id":
                generic_list.append(self.dm_id)
            elif item == "bugs_id":
                generic_list.append(d.GameBugs.id)
            elif item[: len(self.flag)] == self.flag:
                attr = item[len(self.flag) + 1 :]
                generic_list.append(getattr(self.model, attr))
            else:
                generic_list.append(item)
        self.condition = generic_list

    def check_new_section(self):
        """if new section found, set the new section"""
        if self.line[: len(self.flag_section)] == self.flag_section:
            self.set_section_name(
                self.get_socket_arg(self.line, self.flag_section, " #}")
            )

    def set_section_name(self, name: str):
        """
        If the section name is not empty, set the section name to the name provided and create a new list in
        the final dictionary with the section name as the key.

        :param name: The name of the section
        """
        if name != "":
            self.section_name = name
            self.final.update({self.section_name: ""})
            if self.section_name_default in self.final:
                self.final.pop(self.section_name_default)

    def comment_or_empty(self) -> bool:
        """If the line is empty or a comment, return False. Otherwise, return True"""
        if self.line in [" ", ""]:
            return False
        if self.line[:2] == "{#":
            return False
        return True
