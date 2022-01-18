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
    name_form = UserEditName()
    email_form = UserEditEmail()
    pass_form = UserEditPassword()
    del_form = UserDelete()
    return render_template(
        "edit/account/account.html",
        user=current_user,
        name_form=name_form,
        email_form=email_form,
        pass_form=pass_form,
        del_form=del_form,
    )


def account_post():
    with db_session():
        name_form = UserEditName()
        email_form = UserEditEmail()
        pass_form = UserEditPassword()
        del_form = UserDelete()
        user = Users.query.get(current_user.id)
        # these statements are used instead of .validate_on_submit() because otherwise errors from all forms will be displayed
        if name_form.name.data and name_form.validate():
            user.name = name_form.name.data
        elif email_form.email.data and email_form.validate():
            user.update(email=email_form.email.data)
        elif pass_form.password.data and pass_form.validate():
            if pass_form.password.data == pass_form.confirm.data:
                user.update(password=pass_form.password.data)
            else:
                flash("passwords do not match")
        elif del_form.user_delete_submit.data:
            return redirect(url_for("edit.delete_get"))
    return render_template(
        "edit/account/account.html",
        user=current_user,
        name_form=name_form,
        email_form=email_form,
        pass_form=pass_form,
        del_form=del_form,
    )


def delete_get():
    form = UserDelete()
    return render_template("profile/delete.html", form=form)


def delete_post():
    form = UserDelete()
    if not form.validate_on_submit():
        return render_template("profile/delete.html", form=form)
    user = Users.query.get(current_user.id)
    if form.confirm.data == user.email:
        logout_user()
        with db_session:
            user.delete_self()
        flash("Your account has been deleted")
        return redirect(url_for("auth.login"))
    else:
        flash("email does not match")
