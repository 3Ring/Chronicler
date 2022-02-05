from project.helpers.translate_jinja.run import Run


class TranslateJinja(Run):
    def run(self):
        """
        takes html/jinja from chronicler and returns parsed html

        handles jinja: include, comments, if, elif, else, and endif
        Uses jinja comments to direct template parsing:
            {# translate_hook <flag> #}: beginning of template
            {# end_translate_hook <flag> #}: end of template
            {# socket_ignore <flag> #}: templates named <flag> will ignore following lines
            {# endignore <flag> #}: templates named <flag> will stop ignoring lines
            {# translate_section <section_name> #}: beginning of section
            {# endsection <section_name #}: end of section

        jinja variables that this can translate:
                    all variables must be exactly in this format with this spacing or it won't work:
                        "{{ variable }}"
                    (`current_user.id`, `tutorial.id`, `game.dm_id`)
                    and any sqlalchemy class variable attached to the flag arg.
                    ex: if flag == "user" then it can translate user.id, user.email, etc...
                    to add in additional variables use the `**kwarg`

        (these paramaters are passed to the class at instantiation)
        :param model: class instance you want to use for variable replacement
        :param flag: `str` name of the model. Used to determine what jinja comment flags to use
        :param game_id: `Games.id` ID of game
        :param user_id: `Users.id` ID of user submitting the socket
        :param dm_id: `Users.id` of dm
        :param template: `str` of html template file name (this is primarily to change for testing)
        :param target_users: `dict`[`str` identifier, `int` id of target]
                            this is used to create multiple sockets based on the same information.
                            so that it will display differently for different users.
                            ex: {user: current_user.id}
        :param **kwarg: any other variables to be subbed in ex: `char_img = 123`

        :return `dict[dict[str]]`: [`str` target_users identifier, `dict` [`str` section_name, `str` completed html]
                section_name is taken from the jinja comment flags {# translate_section <section_name> #}
        """
        if self.target_users is None:
            return self._run()
        sockets = {}
        for target, _id in self.target_users.items():
            self.reset(_id)
            sockets[target] = self._run()
        return sockets
