class Switch:
    def switch(self, arg_list: list) -> bool:
        """if/elif/else logic (the nesting logic is handed by self.nested_conditional)

        :param arg_list: The list of simplified arguments that are being passed to the function
        :return: The result of the if statement.
        """
        if len(arg_list) > 0:
            if arg_list[0] == "if" or arg_list[0] == "elif":
                arg_list.pop(0)
                if "and" in arg_list or "or" in arg_list:
                    return self._and_or(arg_list)
                else:
                    return self._if(arg_list)

    def _and_or(self, arg_list: list) -> bool:
        """
        delegates the arguement to the and/or functions, splits them up accordingly and evaluates them

        :param arg_list: The list of arguments to be evaluated
        :return: The result of the conditional statement.
        """
        split_on_or = self._or(arg_list)
        conditionals = self._and(split_on_or) if "and" in split_on_or else split_on_or
        for and_group in conditionals:
            for expression in and_group:
                expression = True if self._if(expression) else False
        for and_group in conditionals:
            and_group = False if False in and_group else True
        return True if True in conditionals else False

    def _or(self, arg_list: list) -> list:
        """
        seperates an argument list on the "or" recursively if it is found

        :param arg_list: The list of arguments to be parsed
        :return: A list of seperated lists
        """
        if "or" in arg_list:
            for i, arg in enumerate(arg_list):
                if arg == "or":
                    new_list = [arg_list[:i]]
                    new_list.append([[l] for l in self._or(arg_list[i + 1 :])])
                    return new_list
        return [arg_list]

    def _and(self, arg_list: list) -> list:
        """
        seperates an argument list on the "and" recursively if it is found

        :param arg_list: The list of arguments to be parsed
        :return: A list of seperated lists.
        """
        if "and" in arg_list:
            for i, arg in enumerate(arg_list):
                if arg == "and":
                    new_list = [arg_list[:i]]
                    new_list.append([[l] for l in self._and(arg_list[i + 1 :])])
                    return new_list
        return [arg_list]

    def _if(self, arg) -> bool:
        """
        checks the simplified argument and returns its boolean value

        :param arg: The argument to be evaluated
        :return: A boolean value.
        """
        if type(arg) is list:
            if len(arg) == 1:
                return True if arg[0] else False
            elif len(arg) == 3:
                if arg[1] == "==":
                    return True if arg[0] == arg[2] else False
                elif arg[1] == "!=":
                    return True if arg[0] != arg[2] else False
                elif arg[1] == "<":
                    return True if arg[0] < arg[2] else False
                elif arg[1] == ">":
                    return True if arg[0] > arg[2] else False
                elif arg[1] == "<=":
                    return True if arg[0] <= arg[2] else False
                elif arg[1] == ">=":
                    return True if arg[0] >= arg[2] else False
            else:
                raise BaseException("invalid argument")
        return True if arg else False
