
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, Blueprint
from flask_login import current_user

admin_ = Blueprint("admin_", __name__)

from project.setup_ import defaults as d

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_anonymous:
            return redirect(url_for("index.page"))
        if current_user.id != d.Admin.id:
            return redirect(url_for("index.page"))

        
        return self.render('admin/index.html')
        
@admin_.route("/admin/engage", methods=["GET"])
def engage():
    from project.models import Users, Characters
    for u in Users.query.all():
        chars = Characters.query.filter_by(user_id=u.id).all()
        flag = False
        for c in chars:
            if c.avatar == True:
                flag = True
                av = c.name
        print(f'chars: {c.name} || flag: {flag}')

    return redirect(url_for("admin.index"))
