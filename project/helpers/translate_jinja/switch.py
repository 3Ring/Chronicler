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
