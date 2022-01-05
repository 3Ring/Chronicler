from flask import render_template, redirect, url_for
from flask_login import current_user

from project import forms
from project import form_validators


def get():
    edit_form = forms.UserEdit()
    del_form = forms.UserDelete()
    # form.name.data = current_user.name
    # form.email.data = current_user.email
    # form.password.data = ""
    return render_template(
        "edit/account/account.html",
        user=current_user,
        edit_form=edit_form,
        del_form=del_form,
    )


def post():
    edit_form = forms.UserCreate()
    del_form = forms.UserDelete()
    if del_form.user_delete_submit.data:
        return redirect(url_for("profile.delete"))
    if not form_validators.User.edit(edit_form):
        return redirect(url_for("edit.account"))
    return redirect(url_for("profile.account"))
