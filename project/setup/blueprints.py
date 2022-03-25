

def init_blueprints(app):
    from project.views.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from project.views.index.routes import index as index_blueprint
    app.register_blueprint(index_blueprint)

    from project.views.bugs.routes import bugs as bugs_blueprint
    app.register_blueprint(bugs_blueprint)

    from project.views.profile.routes import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from project.views.edit.routes import edit as edit_blueprint
    app.register_blueprint(edit_blueprint)

    from project.views.create.routes import create as create_blueprint
    app.register_blueprint(create_blueprint)

    from project.views.notes.routes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint)

    from project.views.join.routes import join as join_blueprint
    app.register_blueprint(join_blueprint)
    
    from project.views.admin.routes import admin_ as admin_blueprint
    app.register_blueprint(admin_blueprint)
    return
    
