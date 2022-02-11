from project.helpers.translate_jinja.build_template import Build
from project.helpers.translate_jinja.checks import Checks
from project.helpers.translate_jinja.conditions import Logic
from project.helpers.translate_jinja.convert import Convert


class Run(Build, Checks, Logic, Convert):
    def _run(self):
        """translate_jinja function for each target"""
        # i = 0
        self.line = None
        for line in self.html:
            # self.hold = self.line
            # i += 1
            # if i > 390 and i < 400:
            #     print(i)
            self.line = line
            # if self.line == "{% if note.user_id == current_user.id or note.user_id == tutorial_id %}" and self.target_user == 1:
            #     print(f'yes')
            #     print(f'self.gatekeeper: {self.gatekeeper}')
            #     print(f'self.depth: {self.depth}')
            #     print(f'self.allowed_depth: {self.allowed_depth}')
            #     print(f'self.condition: {self.condition}')
            #     print(f'self.con_type: {self.con_type}')
            #     print(f'type(self.con_type): {type(self.con_type)}')
            if self.check_end():
                break
            if not self.checks():
                # print(f'not checked: {self.line}')
                continue
            generic_line = self.variable_check()
            # if i > 380 and i < 400:
            #     print(f'generic_line: {generic_line}')
            # print(f'generic_line.strip(): {generic_line.strip()}')
            self.final[self.section_name] += generic_line.strip()
        # print(f'self.final: {self.final}')
        return self.final
