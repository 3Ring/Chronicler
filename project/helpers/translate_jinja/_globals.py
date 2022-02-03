from project.setup_ import defaults as d

if_statements = 0
tutorial_id = d.Admin.id
_user_id = int()
_dm_id = int()
_flag = str()
_target_user = int()
ignore = False
sections = dict()
section_name = False
    
def set_globals(flag: str, user_id: int, dm_id: int, target_user: int):
    # global if_statements
    # if_statements = 0
    # global tutorial_id
    # tutorial_id = d.Admin.id
    global _user_id
    _user_id = user_id
    global _dm_id
    _dm_id = dm_id
    global _flag
    _flag = flag
    global _target_user
    _target_user = target_user
    # global ignore
    # ignore = False
    # global sections
    # sections = dict()
    # global section_name
    # section_name = False
    
