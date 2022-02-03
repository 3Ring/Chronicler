from project.helpers.translate_jinja.switch import switch

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
        elif type_ == "if":
            if switch(self.conditionals[self.key]):
                self.passed_if()
            else:
                self.open_failed_if()
        elif type_ == "elif":
            self.open_elif()
        elif type_ == "else":
            self.open_else()

    def gate_closed(self):

        if not self.key in self.conditionals.keys():
            self.remove_line()
            return
        type_ = self.conditionals[self.key][0]
        if type_ == "endif":
            self.closed_endif()
        elif type_ == "if":
            self.closed_if()
        elif type_ == "elif":
            self.closed_elif()
        elif type_ == "else":
            self.closed_else()

    def add_line(self):
        self.final.append(self.html_list[0])
        self.remove_line()

    def remove_line(self):
        self.html_list.pop(0)

    def open_endif(self):
        if self.allowed_depth == self.depth or self.allowed_depth + 1 == self.depth:
            self._elif.pop(self.depth)
            self.allowed_depth += -1
        self.depth += -1
        self.remove_line()

    def passed_if(self):
        self.allowed_depth += 1
        self.depth += 1
        self._elif[self.depth] = False
        self.remove_line()

    def passed_elif(self):
        self.allowed_depth += 1
        self.gatekeeper = True
        self._elif[self.depth] = False
        self.remove_line()

    def open_failed_if(self):

        self.depth += 1
        self._elif[self.depth] = True
        self.gatekeeper = False
        self.remove_line()

    def open_elif(self):
        self.gatekeeper = False
        self.allowed_depth += -1
        self.remove_line()

    def open_else(self):
        self.gatekeeper = False
        self._elif[self.depth] = True
        self.allowed_depth += -1
        self.remove_line()

    def closed_endif(self):
        if self.allowed_depth == self.depth or self.allowed_depth + 1 == self.depth:
            self.gatekeeper = True
            self._elif.pop(self.depth)
            # self.allowed_depth += -1
        self.depth += -1
        self.remove_line()

    def closed_if(self):
        self.depth += 1
        self.remove_line()
        self._elif[self.depth] = False

    def closed_elif(self):
        if self.allowed_depth == self.depth - 1 and self._elif[self.depth]:
            # check to make sure no other ifs have been triggered in this nest
            if switch(self.conditionals[self.key]):
                self.passed_elif()
            else:
                self.closed_failed_elif()
        else:
            self.closed_failed_elif()

    def closed_passed_elif(self):
        self.allowed_depth += 1
        self._elif[self.depth] = False
        self.gatekeeper = True
        self.remove_line()

    def closed_failed_elif(self):
        self.remove_line()

    def closed_passed_else(self):
        self.allowed_depth += 1
        self.gatekeeper = True
        self.remove_line()

    def closed_failed_else(self):
        self.remove_line()

    def closed_else(self):
        if self.allowed_depth == self.depth - 1 and self._elif[self.depth]:
            self.closed_passed_else()
        else:
            self.closed_failed_else()