from flask import redirect, url_for, flash

def not_authorized(message="You are not authorized to access that page", no_flash=False):
    '''
    If the user is not authorized to access the page, redirect them to the index page and flash a
    message
    
    :param message: The message to display to the user, defaults to You are not authorized to access
    that page
    :param no_flash: If you don't want to flash a message, set this to True, defaults to False
    :return: a redirect to the index page.
    '''

    if not no_flash:
        flash(message)
    return redirect(url_for("main.index"))