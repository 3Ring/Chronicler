from flask import render_template, redirect, url_for, flash
from flask_login import current_user, logout_user
from project import defaults as d
from project import forms
from project.models import Users, Games


def get():
    name_form = forms.UserEditName()
    email_form = forms.UserEditEmail()
    pass_form = forms.UserEditPassword()
    del_form = forms.UserDelete()
    return render_template(
        "edit/account/account.html",
        user=current_user,
        name_form=name_form,
        email_form=email_form,
        pass_form=pass_form,
        del_form=del_form,
    )


def post():
    name_form = forms.UserEditName()
    email_form = forms.UserEditEmail()
    pass_form = forms.UserEditPassword()
    del_form = forms.UserDelete()
    user = Users.get_from_id(current_user.id)
    # these statements are used instead of .validate_on_submit() because otherwise errors from all forms will be displayed
    if name_form.name.data and name_form.validate():
        user.update(name=name_form.name.data)
    elif email_form.email.data and email_form.validate():
        user.update(email=email_form.email.data)
    elif pass_form.password.data and pass_form.validate():
        if pass_form.password.data == pass_form.confirm.data:
            user.update(password=pass_form.password.data)
        else:
            flash("passwords do not match")
    elif del_form.user_delete_submit.data:
        return redirect(url_for("edit.delete"))
    return render_template(
        "edit/account/account.html",
        user=current_user,
        name_form=name_form,
        email_form=email_form,
        pass_form=pass_form,
        del_form=del_form,
    )


def confirm_get():
    form = forms.UserDelete()
    return render_template("profile/delete.html", form=form)

def confirm_post():
    form = forms.UserDelete()
    if form.validate_on_submit():
        user = Users.get_from_id(current_user.id)
        if form.confirm.data == user.email:
            logout_user()
            user.delete_self(confirm=True)
            return redirect(url_for("auth.login"))
        else:
            flash("email does not match")
    return render_template("edit/account/delete.html", form=form)
