from flask import render_template, redirect, request
from flask_login import confirm_login

from project.forms.login import Login


def reauth_get():
    """
    redirects user to login page when they need to reauthenicate their session

    this is called when trying to access sensative information
    :return: The rendered login.html template.
    """
    form = Login()
    return render_template("auth/reauth.html", form=form)


def reauth_post():
    """
    Refreshed the user's session and redirects them to the page they were originially trying to access upon successful form validation.

    :return: a redirect the page that requested the reauthentication.
    """
    form = Login()
    if not form.validate_on_submit():
        return render_template("auth/reauth.html", form=form)
    confirm_login()
    return redirect(request.args.get("next"))
