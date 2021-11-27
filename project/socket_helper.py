import os
from project.helpers import private_convert
from project.models import Users

if_statements = 0
def get_tutorial_id():
    return Users.get_admin().id
user_id = None
dm_id = None
current_user = None

# main funtion
def translate_jinja(model, flag, game_id, u_id=None, d_id=None, c_user=None, **kwarg):
    '''takes html from chronicler and returns handles: if, elif, else
    model: class instance you want to use for variable replacement
    flag: string with the name of the model
    u_id: current_user.id
    d_id: dm_id
    **arg any other variables to be subbed in ex: char_img = 123'''
    
    global if_statements
    tutorial_id = get_tutorial_id()
    global user_id
    global dm_id
    global current_user

    user_id = u_id
    dm_id = d_id
    current_user = c_user

    # compile html pages into one list
    html_list = build_notes_template("blueprint.html")

    final_sockets = find_sections_to_translate(html_list, flag)
    finished = {}
    for name, html in final_sockets.items():
        finished[name] = finalize(html, model, flag, game_id, **kwarg)
    return finished


# general helper function
# returns interior of string when start matched line prefix
# otherwise it returns false
def get_socket_arg(line, start, end):
    if line[:len(start)] == start:
        arg = line[len(start):(len(end) * -1)]
        args = arg.split(" ")
        return_args = []
        if len(args) > 1:
            for line in args:
                strip = line.strip()
                if strip == "" or strip == " ":
                    pass
                else:
                    return_args.append(strip)
        if len(return_args) > 1:
            return return_args
        else:
            return line[len(start):(len(end) * -1)]
    else:
        return False


# acquire and build template function
# 
# compiles templates recursively into one list
# file name is the filename in the notes directory of templates ex: "blueprint.html"
# this will only work in notes.html but can be easily changed for another page if needed
def build_notes_template(filename):

    raw_html  = build_notes_template_get(filename)
    cleaned_list = build_notes_template_clean(raw_html)
    new_list = build_notes_template_read(cleaned_list)
    return new_list

# helper function
# takes raw html and jinja and converts it into a list. Removing trailing and ending whitespace
def build_notes_template_clean(html):
    file_list = html.split("\n")
    cleaned = []
    
    for line in file_list:
        stripped = line.strip()
        if stripped == "" or stripped == " ":
            pass
        else:
            cleaned.append(stripped)
    return cleaned

# helper function
# finds and opens the jinja template
def build_notes_template_get(filename):
    # get file
    templates_path = "templates/notes"
    root_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(root_dir, templates_path)
    src = os.path.join(templates_dir, filename)
    return open(src).read()


# helper function
# read page and find the "include" jinja links
def build_notes_template_read(html_list):
    # flag = "{% include 'notes/"
    # end_flag = "' %}"

    for i, line in enumerate(html_list):

        path = get_socket_arg(line, "{% include 'notes/", "' %}")
        if path:
            next_html = build_notes_template(path)
            list_1 = html_list[:i]
            list_2 = html_list[i+1:]
            final_list = list_1 + next_html + list_2
            
            return build_notes_template_read(final_list)
    return html_list

# ######


# functions to get relevant sections(s)
# 
# the flag is the model name ex: "note" or "session"
def find_sections_to_translate(html_list, flag):
    scoped_html_list = set_socket_scope(html_list)

    start = find_html_start(scoped_html_list, flag)
    end = find_html_end(scoped_html_list, flag)
    pruned_html = scoped_html_list[start:end]

    # returns a list of lists. if there is only one section it will return [[section]]
    sections = set_sections(pruned_html, flag)

    return sections

# helper function
# prunes all html except for those inside of the {# socket_scope #}
def set_socket_scope(html):

    scope_start = html.index("{# socket_scope start #}")
    scope_end = html.index("{# socket_scope end #}")
    return html[scope_start+1:scope_end]

# helper function
# finds the start of the relevant html
# returns index
def find_html_start(html_list, flag):
    for i, line in enumerate(html_list):
        hook = "{# translate_hook " + flag + " #}"
        found = line.find(hook)
        if found != -1:
            return i+1
    raise "socket flag not found"

# helper function
# finds end of relevant html
# returns index
def find_html_end(html_list, flag):

    for i, line in enumerate(html_list):
        hook = "{# end_translate_hook " + flag + " #}"
        found = line.find(hook)
        if found != -1:
            return i
    raise "socket flag not found"

# helper functions
# called by set_sections() to flag ignored sections
def check_ignore_start(html_line, flag):

    if html_line == "{# socket_ignore " + flag + " #}":
        return True
    else:
        return False
def check_ignore_stop(html_line, flag):

    if html_line == "{# endignore " + flag + " #}":
        return True
    else:
        return False

# helper function
# cuts out ignored sections and splits relevant areas into a list.
# returns a list of length = 1 if nothing is ignored
def set_sections(html_list, flag):


    section_end_flag = "{# endsection " + flag + " #}"
    ignored = False
    new_section_discovered = False
    section = {}
    section["no_sections"] = []
    for line in html_list:

        # check if the line should be ignored or not and then.
        # this works with the Jinja comment flags {# socket_ignore <flag> #} and {# endignore <flag> #}
        if ignored:
            if check_ignore_stop(line, flag):
                ignored = False
            continue
        else:
            if check_ignore_start(line, flag):
                ignored = True
                continue
            else:
                not_ignored = line

        # check if a new section is flagged
        # this works with the Jinja comment flags {# translate_section <flag> <section_name>#} and {# endsection <flag> #}
        if new_section_discovered:
            if not_ignored == section_end_flag:
                new_section_discovered = False
                
            else:
                section[new_section_discovered].append(not_ignored)
        else:

            new_section_discovered = get_socket_arg(not_ignored, "{# translate_section ", " #}")

            
            if new_section_discovered:
                if type(new_section_discovered) == list:
                    new_section_discovered = new_section_discovered[1]
                    section[new_section_discovered] = eval("new_section_discovered")
                    section[new_section_discovered] = []
                
            # usually the section would be set as the first line
            # if there is already lines commited without a section, this will add those lines as the first list(section)
            else:
                section["no_sections"].append(not_ignored)
    if len(section["no_sections"]) == 0:
        section.pop("no_sections")
    return section



def _or(arg_list):
    new_list = []
    if "or" in arg_list:
        for i, arg in enumerate(arg_list):
            if arg == "or":
                new_list.append(arg_list[:i])
                return_lists = _or( arg_list[i+1:] )
                for l in return_lists:
                    new_list.append(l)
                return new_list

    else:
        return [arg_list]


def _and( arg_list ):
    new_list = []
    if "and" in arg_list:
        for i, arg in enumerate(arg_list):
            if arg == "and":
                new_list.append(arg_list[:i])
                return_lists = _and( arg_list[i+1:] )
                for l in return_lists:
                    new_list.append(l)
                return new_list
    else:
        return [arg_list]

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
            raise "invalid argument"

    else:
        if a:
            return True
        else:
            return False

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
# functions to compile html pages together
# 
# 

# returns a list of conditionals from jinja
def get_jinja_conditional_list(line):

    if line[0:2] == "{%" and line[len(line)-2:] == "%}":
        conditional = line[2:-2]
        conditional.strip()
        conditional_list = conditional.split(" ")

        for i, word in enumerate(conditional_list):
            if word == " " or word == "":
                conditional_list.pop(i)
            word = word.strip()

        return conditional_list
    return False

def make_generic_variable(line, flag):
    marker = f" {flag}."
    replacer = f" model."
    made_generic = line.replace(marker, replacer)

    return made_generic

    

def convert_flag_to_generic(model, flag, **lists):


    generic_list = []
    index = 0
    for key, _list in lists.items():

        index += 1
        if key == "conditional_list":
            list_type = "conditional"
        else:
            list_type = "socket"
    if list_type == "conditional":
        
        for item in _list:
            if item.lower() == "true" or item.lower() == "false":
                generic_list.append(private_convert(item))
            elif item == "current_user.id":
                generic_list.append(current_user)
            elif item == "tutorial.id":
                generic_list.append(get_tutorial_id())
            elif item == "game.dm_id":
                generic_list.append(dm_id)
            elif item[:len(flag)] == flag:
                generic_str = eval(f"model{item[len(flag):]}")
                generic_list.append(generic_str)
            else:
                generic_list.append(item)
    else:
        
        if _list.find(f" {flag}.") != -1:
            return make_generic_variable(_list, flag)
        else:
            return _list
    return generic_list

def stringify_and_add_whiteSpace(string_list):
    space_added = ""
    for word in string_list:
        space_added += word + " "
    stripped = space_added.strip()
    return stripped

def check_for_start_or_end(conditional_list):
    for item in conditional_list:
        if item == "endif" or item == "if":
            return item



def update_statements(condition):

    global if_statements

    if condition == "endif":
        change = -1
    elif condition == "if":
        change = 1
    else:
        raise "not valid condition"

    if condition == "if" or condition == "endif":
        if_statements += change



def group_commands(commands):

    if_starts = [] 
    # get locations of the end of if statements
    depth = -1
    e_index = 0
    s_index = 0
    deepest = 0
    pairs = {}
    for key, value in commands.items():

        if value[0] == 'if':
            depth += 1
            if_starts.append((s_index, depth, key, 'if'))
            pairs[key] = {}
            pairs[key]["type"] = 'if'
            pairs[key]["depth"] = depth
            pairs[key]["index"] = s_index
            if depth > deepest:
                deepest = depth
            s_index += 1
        elif value[0] == 'elif':

            if_starts.append((s_index, depth, key, 'elif'))
            pairs[key] = {}
            pairs[key]["type"] = 'elif'
            pairs[key]["depth"] = depth
            pairs[key]["index"] = s_index
            s_index += 1
        
        elif value == ['else']:

            if_starts.append((s_index, depth, key, 'else'))
            pairs[key] = {}
            pairs[key]["type"] = 'else'
            pairs[key]["depth"] = depth
            pairs[key]["index"] = s_index
            s_index += 1

        elif value == ['endif']:
            
            if_starts.append((e_index, depth, key, 'endif'))
            pairs[key] = {}
            pairs[key]["type"] = 'endif'
            pairs[key]["depth"] = depth
            pairs[key]["index"] = e_index
            depth += -1
            e_index += 1

    return if_starts


def append_commands(grouped, by_depth):
    expression_index = 0
    depth = 1
    html_index = 2
    _type = 3
    command_meta = {}
    # whole list
    ends = []
    for i, depth_list in enumerate(by_depth):
        # depth list
        ends.append([])
        for meta in depth_list:

            if meta[_type] == "if":
                # statement list
                ends[i].append([])
                ends[i][-1].append(meta[html_index])
            elif meta[_type] == "elif":
                ends[i][-1].append(meta[html_index])
            elif meta[_type] == "else":
                ends[i][-1].append(meta[html_index])
            if meta[_type] == 'endif':
                ends[i][-1].append(meta[html_index])



    for command_list in grouped:


        i = command_list[html_index]
        command_meta[i] = {}
        command_meta[i]["type"] = command_list[_type]
        command_meta[i]["depth"] = command_list[depth]
        command_meta[i]["index"] = command_list[expression_index]
        for statement_list in ends[command_list[depth]]:
            if i in statement_list:
                command_meta[i]["end"] = statement_list[-1]
                break
    return command_meta
        
def apply_commands(commands, command_meta, html_list, key=0, depth=0):


    socket = []
    sub_socket = []
    i = key
    j = key + 1
    gatekeeper = True

    while i < len(html_list):

        if i in commands.keys():

            if commands[i][0] == "if" and command_meta[i]["depth"] == depth:
                if not gatekeeper:

                    if key - 1 in command_meta.keys():
                    

                        depth += 1
                        i += 1
                        continue
                    else:
                        gatekeeper = True
                        continue


                elif switch(commands[i]):

                    gatekeeper = True

                    if len(sub_socket) > 0:

                        socket.append(sub_socket)
                        sub_socket = []

                    temp = apply_commands(commands, command_meta, html_list[:command_meta[i]["end"]], key=j, depth=depth+1)
                    for _list in temp:
                        socket.append(_list)


                    i = command_meta[i]["end"] + 1
                    j = i + 1

                    continue
                else:

                    gatekeeper = False
            elif commands[i][0] == "elif"  and command_meta[i]["depth"] == depth:

                if switch(commands[i]):

                    gatekeeper = True

                    if len(sub_socket) > 0:
                        socket.append(sub_socket)
                        sub_socket = []
                    temp = apply_commands(commands, command_meta, html_list[:command_meta[i]["end"]], key=j, depth=depth+1)

                    for _list in temp:
                        socket.append(_list)

                    i = command_meta[i]["end"] + 1
                    j = i + 1

                    continue
                else:
                    gatekeeper = False
            elif commands[i][0] == "else" and command_meta[i]["depth"] == depth:

                gatekeeper = True

                if len(sub_socket) > 0:
                    socket.append(sub_socket)
                    sub_socket = []
                temp = apply_commands(commands, command_meta, html_list[:command_meta[i]["end"]], key=j, depth=depth+1)
                for _list in temp:
                    socket.append(_list)

                i = command_meta[i]["end"] + 1
                j = i + 1

                continue
            else:
                gatekeeper = False
                if commands[i] == ["endif"] and depth == command_meta[i]["depth"]:
                    gatekeeper = True


            
        elif gatekeeper:
            sub_socket.append(html_list[i])
            
        i+=1
        j+=1

    socket.append(sub_socket)
    sub_socket = []

    return socket

def group_by_depth(if_condtions):
    if len(if_condtions) == 0:
        return None
    commands = []
    start = 0
    pop_list = []
    for i, line in enumerate(if_condtions):
        if line[3] == 'if':
            start += 1
        elif line[3] == 'endif':
            if start == 1:
                commands.append(line)
                pop_list.append(i)
                start += -1
                continue
            else:
                start += -1
        if start != 1:
            continue
        else:
            if line[3] == 'if':
                commands.append(line)
                pop_list.append(i)
            elif line[3] == 'elif':
                commands.append(line)
                pop_list.append(i)
            elif line[3] == 'else':
                commands.append(line)
                pop_list.append(i)

    pop_list.reverse()
    for pop in pop_list:
        if_condtions.pop(pop)
    temp = group_by_depth(if_condtions)
    if temp is None:
        return [commands]
    else:
        final = [commands]
        for _list in temp:
            final.append(_list)
        return final      

def remove_jinja_comments(html):

    new = []
    for line in html:
        if line[:2] == "{#" or line == "" or line == " ":
            pass
        else:
            new.append(line)
    
    return new

def convert_to_socket(html, model, flag):

    htmlWithout_jinja_comments = remove_jinja_comments(html)
    generic_socket = []
    for line in htmlWithout_jinja_comments:
        generic_socket.append(convert_flag_to_generic(model, flag, socket_list=line))

    return generic_socket



def pass_model_variables(html, model, game_id, **additional_keys):
    html = html
    columns = {}
    for column in model.__table__.columns:
        columns[str(column.key)] = getattr(model, str(column.key))
    
    # iterate through each key/value pair in the model instance's attributes
    i = 0
    while i < len(html):

        for key, value in columns.items():
            model_key = "{{ " + "model." + key + " }}"
            currentU_key = "{{ " + "current_user.id" " }}"
            gameID_key = "{{ " + "id" " }}"

            # replace jinja variables
            # if 
            html[i] = html[i].replace(model_key, str(value))
            html[i] = html[i].replace(currentU_key, str(current_user))
            html[i] = html[i].replace(gameID_key, str(game_id))
        for key2, value in additional_keys.items():
            arg_key = "{{ " + "model." + str(key2) + " }}"
            html[i] = html[i].replace(arg_key, str(getattr(model, str(key2))))

        i+=1
    
    return html


def finalize(html, model, flag, game_id, **kwarg):

    commands = {}
    for i, line in enumerate(html):
            conditional_list = get_jinja_conditional_list(line)

            if conditional_list:

                start_or_end = check_for_start_or_end(conditional_list)
                
                if start_or_end:

                    update_statements(start_or_end)


                generic_conditional_list = convert_flag_to_generic(model, flag, conditional_list=conditional_list)
                
                commands[i] = generic_conditional_list

    if if_statements != 0:
        raise "nesting error. statements are not even"

    if conditional_list:
        grouped_commands = group_commands(commands)

        copied_commands = []
        for line in grouped_commands:
            copied_commands.append(line)

        commands_by_depth = group_by_depth(grouped_commands)

        appended_commands = append_commands(copied_commands, commands_by_depth)

        section = apply_commands(commands, appended_commands, html)

        cleaned_section = []
        while len(section) > 0:
            temp = section[0]
            section.pop(0)
            for sub in temp:
                cleaned_section.append(sub)


        generic_socket_list = convert_to_socket(cleaned_section, model, flag)
    else:
        generic_socket_list = convert_to_socket(html, model, flag)

    final_socket_list = pass_model_variables(generic_socket_list, model, game_id, **kwarg)

    final_socket = stringify_and_add_whiteSpace(final_socket_list)

    return final_socket
    


