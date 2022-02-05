class Logic:
    def nested_conditionals(self):
        """if/elif/else nesting logic to determine if self.line is appended to the socket"""
        self.top_checks()
        if self.gatekeeper:
            if self.con_type is None:
                return True
            if self.con_type == "endif":
                return self.open_endif()
            elif self.con_type == "if":
                self.passed_if() if self.switch(self.condition) else self.open_failed_if()
            elif self.con_type == "elif":
                self.open_elif()
            elif self.con_type == "else":
                self.open_else()
        else:
            if self.con_type is None:
                pass
            elif self.con_type == "endif":
                self.closed_endif()
            elif self.con_type == "if":
                self.closed_if()
            elif self.con_type == "elif":
                self.closed_elif()
            elif self.con_type == "else":
                self.closed_else()
        return False

    def closed_passed_else(self):
        self.allowed_depth += 1
        self.gatekeeper = True
        
    def closed_failed_else(self):
        pass

    def closed_else(self):
        if self.allowed_depth == self.depth - 1 and self._elif[self.depth]:
            self.closed_passed_else()
        else:
            self.closed_failed_else()

    def closed_elif(self):
        if self.allowed_depth == self.depth - 1 and self._elif[self.depth]:
            self.passed_elif() if self.switch(self.condition) else self.closed_failed_elif()
        else:
            self.closed_failed_elif()

    def closed_failed_elif(self):
        pass

    def passed_elif(self):
        self.allowed_depth += 1
        self.gatekeeper = True
        self._elif[self.depth] = False

    def closed_if(self):
        self.depth += 1
        self._elif[self.depth] = False

    def closed_endif(self):
        if self.allowed_depth == self.depth or self.allowed_depth + 1 == self.depth:
            self.gatekeeper = True
            self._elif.pop(self.depth)
        self.depth += -1

    def open_else(self):
        self.gatekeeper = False
        self._elif[self.depth] = True
        self.allowed_depth += -1

    def open_elif(self):
        self.gatekeeper = False
        self.allowed_depth += -1

    def open_failed_if(self):
        self.depth += 1
        self._elif[self.depth] = True
        self.gatekeeper = False

    def passed_if(self):
        self.allowed_depth += 1
        self.depth += 1
        self._elif[self.depth] = False

    def open_endif(self):
        if self.allowed_depth == self.depth or self.allowed_depth + 1 == self.depth:
            self._elif.pop(self.depth)
            self.allowed_depth += -1
        self.depth += -1
