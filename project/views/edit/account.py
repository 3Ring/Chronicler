from sys import prefix
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, logout_user

from project.helpers.db_session import db_session
from project.forms.edit_user import (
    UserEditEmail,
    UserEditName,
    UserEditPassword,
    UserDelete,
)
from project.models import Users
from project.helpers.db_session import db_session


def account_get():
    """
    GET request function for "edit/account/account.html"

    This function renders the account settings page

    :return: The rendered account.html template
    """
    name_form = UserEditName(prefix="name")
    email_form = UserEditEmail(prefix="email")
    pass_form = UserEditPassword(prefix="pass")
    del_form = UserDelete(prefix="del")
    return render_template(
        "edit/account/account.html",
        user=current_user,
        name_form=name_form,
        email_form=email_form,
        pass_form=pass_form,
        del_form=del_form,
    )


def account_post():
    """
    POST request function for "edit/account/account.html"

    This function is used to edit the user's account information.
    :return: The rendered account.html template.
    """
    with db_session():
        name_form = UserEditName(prefix="name")
        email_form = UserEditEmail(prefix="email")
        pass_form = UserEditPassword(prefix="pass")
        del_form = UserDelete(prefix="del")
        user = Users.query.get(current_user.id)
        if name_form.submit.data and name_form.validate():
            user.name = name_form.name.data
        elif email_form.submit.data and email_form.validate():
            user.email = email_form.email.data
        elif pass_form.submit.data and pass_form.validate():
            user.password = pass_form.password.data
        elif del_form.submit.data and del_form.validate():
            return redirect(url_for("edit.delete"))
        return render_template(
            "edit/account/account.html",
            name_form=name_form,
            email_form=email_form,
            pass_form=pass_form,
            del_form=del_form,
        )


def delete_get():
    """
    GET request function for "edit/account/account.html"

    This function is used to access the delete accound page
    :return: The rendered delete.html template.
    """
    form = UserDelete()
    return render_template("edit/delete.html", form=form)


def delete_post():
    """
    POST request function for "edit/account/account.html"

    Delete the user's account and log them out
    :return: redirect to login page.
    """
    form = UserDelete()
    if not form.validate_on_submit():
        return render_template("edit/delete.html", form=form)
    user = Users.query.get(current_user.id)
    logout_user()
    with db_session():
        user.delete_self()
        flash("Your account has been deleted")
        return redirect(url_for("auth.login"))
