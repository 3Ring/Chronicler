
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, Blueprint, flash
from flask_login import current_user

admin_ = Blueprint("admin_", __name__)

from project.setup_ import defaults as d

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self, var=None):
        if current_user.is_anonymous:
            return redirect(url_for("index.page"))
        if current_user.id != d.Admin.id:
            return redirect(url_for("index.page"))

        
        return self.render('admin/index.html', var=var)
    
@admin_.route("/admin/engage", methods=["GET"])
def engage():
    from project.models import Users, Characters
    var = []
    for u in Users.query.all():
        chars = Characters.query.filter_by(user_id=u.id).all()
        flag = False
        for c in chars:
            if c.avatar == True:
                flag = True
        var.append(f'chars: {c.name} || flag: {flag}')
    flash(f'var: {var}')
    return redirect(url_for("admin.index"))
