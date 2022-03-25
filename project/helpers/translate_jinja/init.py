from project.setup import defaults as d


class Init():
    def __init__(self, model, flag: str, game_id: int, user_id: int = None, dm_id: int = None, target_user: int = None, target_users: dict = None, template: str = "blueprint.html"):
        self.model = model
        self.flag = flag
        self.game_id = game_id
        self.user_id = user_id
        self.dm_id = dm_id
        self.target_user = target_user
        self.target_users = target_users
        self.scope_found = False
        self.hook_found = False
        self._ignore = False
        self.con_type = None
        self.condition = []
        self.key = 0
        self.depth = 0
        self.allowed_depth = 0
        self.gatekeeper = True
        self._elif = {}
        self.tutorial_id = d.Admin.id
        self.flag_scope = "{# socket_scope start #}"
        self.flag_section = "{# translate_section " + self.flag
        self.section_name_default = "no_sections"
        self.flag_hook = "{# translate_hook " + self.flag
        self.flag_hook_end = "{# end_translate_hook " + self.flag + " #}"
        self.flag_ignore = "{# socket_ignore " + self.flag + " #}"
        self.flag_ignore_end = "{# endignore " + self.flag + " #}"
        self.section_name = self.section_name_default
        self.final = {self.section_name: ""}

    def reset(self, target_user):
        self.scope_found = False
        self.hook_found = False
        self._ignore = False
        self.con_type = None
        self.condition = []
        self.key = 0
        self.depth = 0
        self.allowed_depth = 0
        self.gatekeeper = True
        self._elif = {}
        self.target_user = target_user
        self.section_name = self.section_name_default
        self.final = {self.section_name: ""}