from project.helpers.translate_jinja import _globals
from project.helpers.translate_jinja.build_template import build_template
from project.helpers.translate_jinja.prune_template import prune_template
from project.helpers.translate_jinja.insert_variables import finalize


def translate_jinja(
    model,
    flag: str,
    game_id: int,
    user_id: int = None,
    dm_id: int = None,
    template: str = "blueprint.html",
    target_users: dict = None,
    **kwarg,
):
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
                (`current_user.id`, `tutorial.id`, `game.dm_id`)
                and any sqlalchemy class variable attached to the flag arg.
                ex: if flag == "user" then it can translate user.id, user.email, etc...
                to add in additional variables use the `**kwarg`

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
    if not target_users:
        return run(
            model,
            flag,
            game_id,
            user_id=user_id,
            dm_id=dm_id,
            template=template,
            **kwarg,
        )

    sockets = {}
    for target, id_ in target_users.items():
        sockets[target] = run(
            model,
            flag,
            game_id,
            user_id=user_id,
            dm_id=dm_id,
            template=template,
            target_user=id_,
            **kwarg,
        )
    return sockets


def run(
    model,
    flag: str,
    game_id: int,
    user_id: int = None,
    dm_id: int = None,
    target_user: int = None,
    template: str = "blueprint.html",
    **kwarg,
):
    """creates socket for target_user"""

    _globals.set_globals(flag, user_id, dm_id, target_user)
    html_list = build_template(template)

    raw_sections = prune_template(html_list)
    finished = {}
    for name, section in raw_sections.items():
        finished[name] = finalize(section, model, game_id, **kwarg)
    return finished
