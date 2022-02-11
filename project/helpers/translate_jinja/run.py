from project.helpers.translate_jinja.build_template import Build
from project.helpers.translate_jinja.checks import Checks
from project.helpers.translate_jinja.conditions import Logic
from project.helpers.translate_jinja.convert import Convert


class Run(Build, Checks, Logic, Convert):
    def _run(self):
        """translate_jinja function for each target"""
        self.line = None
        for line in self.html:
            self.line = line
            if self.check_end():
                break
            if not self.checks():
                continue
            generic_line = self.variable_check()
            self.final[self.section_name] += generic_line.strip()
        return self.final
