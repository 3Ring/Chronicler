from flask import render_template, redirect, request
from flask_login import confirm_login

from project.forms.login import Login


def reauth_get():
    form = Login()
    return render_template("login.html", form=form)


def reauth_post():
    form = Login()
    if not form.validate_on_submit():
        return render_template("login.html", form=form)
    confirm_login()
    return redirect(request.args.get("next"))
