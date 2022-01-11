
def init_blueprints(app):
    from project.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from project.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from project.views.bugs import bugs as bugs_blueprint
    app.register_blueprint(bugs_blueprint)

    # from project.views.admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint)

    from project.views.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from project.views.edit import edit as edit_blueprint
    app.register_blueprint(edit_blueprint)

    from project.views.create import create as create_blueprint
    app.register_blueprint(create_blueprint)

    from project.views.notes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint)

    from project.views.join import join as join_blueprint
    app.register_blueprint(join_blueprint)
    
    return
    
