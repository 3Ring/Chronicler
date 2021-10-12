from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
import os
import json
from .events import *
from .classes import *
from flask_login import login_required, current_user
from . import db
from .helpers import upload, nuke, new_game_training_wheels, attach_game_image_or_default_from_Images_model


# Variables
db_password = os.environ.get('DB_PASS')
decoder = "data:;base64,"

imageLink__defaultCharacter = "/static/images/default_character.jpg"
imageLink__defaultGame = "/static/images/default_game.jpg"
imageLink__defaultDm = "/static/images/default_dm.jpg"
imageLink__buttonEdit = "/static/images/edit_button_image.png"


main = Blueprint('main', __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        games=Games.query.filter(
            Games.dm_id != current_user.id,
            Games.id.in_(
            Players.query.with_entities(Players.games_id).
            filter(Players.users_id.in_(
            Users.query.with_entities(
            Users.id).filter_by(
            id=current_user.id))))
        ).all()
        dm_games=Games.query.filter_by(dm_id=current_user.id).all()

        # set images for game the lists
        for game in games:
            img = Images.query.filter_by(id=game.img_id).first()
            if not img:
                game.image = imageLink__defaultGame
            else:
                game.image = decoder + img.img
        for game in dm_games:
            img = Images.query.filter_by(id=game.img_id).first()
            if not img:
                game.image = imageLink__defaultGame
            else:
                game.image = decoder + img.img

        return render_template("index.html"
            , ty=type
            , lis=list
            , games=games
            , dm_games=dm_games)

    return redirect(url_for('auth.login'))

# create database
# @main.route('/initdb')
# def initdb_p():

#     # import psycopg2
#     from .helpers import init_training_wheels_db
#     # from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

#     # # Connect to PostgreSQL DBMS

#     # con = psycopg2.connect(f"host='chronicler_host' user='postgres' password='{db_password}'")
#     # con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

#     # # Obtain a DB Cursor
#     # cursor          = con.cursor()
#     # name_Database   = "chronicler_db"

#     # # Create table statement

#     # cursor.execute(f"DROP DATABASE IF EXISTS {name_Database};")
#     # sqlCreateDatabase = "create database "+name_Database+";"
#     # cursor.execute(sqlCreateDatabase)
#     # print(f"{name_Database} created")
#     # return "need to run db upgrade"

#     # Create a table in PostgreSQL database

#     # This is really hackish. I would like to run flask db upgrade automatically but this will do for now
#     # exits until db upgrade is

#     init_training_wheels_db()
#     return 'init localhost database'


    

@main.route('/join/<int:id>', methods = ['POST', 'GET'])
@login_required
def join(id):
    if id == 0:
        games=Games.query.filter(Games.dm_id != current_user.id).all()
        for game in games:
            img_id = Images.query.filter_by(id=game.img_id).first()
            game.image = attach_game_image_or_default_from_Images_model(img_id)
        return render_template("join.html"
            , games=games
        )
    else:
        return redirect(url_for('main.joining', id=id))


@main.route('/joining/<int:id>', methods = ['GET', 'POST'])
@login_required
def joining(id):
    image_form_name = 'img'
    charform=CharForm()
    game=Games.query.filter_by(id=id).first()
    if request.method=='GET':
         
        # set images for game
        img = Images.query.filter_by(id=game.img_id).first()
        if not img:
            game.image = imageLink__defaultGame
        else:
            game.image = decoder + img.img
        return render_template('joining.html',
            charform=charform,
            game=game)
    if charform.charsubmit.data:
        if charform.img.data:

            image_id = upload(image_form_name)

            if type(image_id) != int:
                flash(image_id)
                return redirect(url_for('main.joining', id=id))

            character=Characters(name=charform.name.data, img_id=image_id, bio=charform.bio.data, user_id=current_user.id, game_id=id)
            db.session.add(character)
            db.session.commit()

        else:
            character=Characters(name=charform.name.data, bio=charform.bio.data, user_id=current_user.id, game_id=id)
            db.session.add(character)
            db.session.flush()
            
        player=Players(users_id=current_user.id, games_id=id)
        db.session.add(player)
        db.session.commit()
        flash("{0} has joined the {1}!!".format(charform.name.data, game.name), "alert-success")
        return redirect(url_for('main.notes', id=game.id))

@main.route('/create', methods=["GET", "POST"])
@login_required
def create():

    gameform=CreateGameForm()
    upload_name = "img"
    if request.method=="GET":
        return render_template('create.html',
            gameform=gameform)
    else:
        if gameform.img.data:
            image_id = upload(upload_name) 
            if type(image_id) != int:
                flash(image_id)
                return redirect("/create")
            game=Games(name=gameform.name.data, dm_id=current_user.id, img_id=image_id, published=gameform.published.data)
        else:
            game=Games(name=gameform.name.data, dm_id=current_user.id, published=gameform.published.data)

        db.session.add(game)
        db.session.flush()
        dm_char=Characters(name="DM", user_id=current_user.id, game_id=game.id)
        db.session.add(dm_char)
        playerlist=Players(users_id=current_user.id, games_id=game.id)
        db.session.add(playerlist)
        db.session.commit()

        # add tutorial notes and session zero to game
        new_game_training_wheels(game)

        return redirect(url_for('main.notes', id=game.id))


from .helpers import make_character_images

@main.route('/notes/<id>', methods = ['GET'])
@login_required
def notes(id):
    # figure out how many sessions there are and if they have any notes attached to them
    session_titles=Sessions.query.filter_by(games_id=id).order_by(Sessions.number).all()


    # get game info
    game=Games.query.filter_by(id=id).first()
    if game.img_id:
        image=Images.query.filter_by(id=game.img_id).first()
        game.image = attach_game_image_or_default_from_Images_model(image)

    # get note info
    logs = {}
    tutorial = Users.query.filter_by(email="app@chronicler.gg").first()
    if session_titles == None:
        pass
    else:
        if type(session_titles) != list:
            session_titles.number=str(session_titles.number)
            logs[str(session_titles.number)] = Notes.query.filter_by(game_id=id).filter_by(session_number=session_titles.number).all()

        else:
            for session in session_titles:
                notes = Notes.query.filter_by(game_id=id).filter_by(session_number=session.number).order_by(Notes.date_added).all()
                logs[str(session.number)] = notes

            if len(session_titles) > 1:
                session_titles.reverse()
            # Set as strings so that they can be used as dict keys
            for session in session_titles:
                session.number=str(session.number)
    # add images to notes
    for session, note in logs.items():


        if type(logs[session]) == list:
            for note in logs[session]:

                note.char_img = make_character_images(note.character)
        else:

            session.char_img = make_character_images(session.character)



    # connvert notes to JSON so that the js script attached to notes.html can insert the rich text.
    # This has to be done because otherwise the html won't be able to read the mark up
    js_logs = {}
    for session in logs:
        if type(logs[session]) == list:
            js_logs[session] = []
            for note in logs[session]:
                js_logs[session].append([note.id, note.note])
        else:
            js_logs[session] = [note.id, note.note]
    js_note_dict = json.dumps(js_logs)

    return render_template('notes/main.html'
        , tutorial=tutorial
        , js_note_dict=js_note_dict
        , edit_img=imageLink__buttonEdit
        , note_dict=logs
        , id=id
        , session_titles=session_titles
        , game=game
    )

@main.route('/profile')
@login_required
def profile():
    user = Users.query.filter_by(id=current_user.id).first()
    return render_template('profile.html'
        , user=user
    )

@main.route('/test_tables', methods = ['GET', 'POST'])
@login_required
def test_tables():

    # make sure that only the admin can access this site
    if not current_user.id == 1:
        return redirect(url_for('main.profile'))
    
    # set variable so Flask can build the site
    uservalues=Users().values
    userheads = Users().head
    users = Users.query.all()
    gameheads = Games().head
    games = Games.query.all()
    characterheads = Characters().head
    characters = Characters.query.all()
    npcheads = NPCs().head
    npcs = NPCs.query.all()
    placeheads = Places().head
    places = Places.query.all()
    lootheads = Loot().head
    loots = Loot.query.all()
    noteheads = Notes().head
    notes = Notes.query.all()
    playersheads=Players().head
    players = Players.query.all()
    sessionheads=Sessions().head
    sessions=Sessions.query.all()

    userform = UserForm()
    gameform = GameForm()
    charform = CharForm()
    npcform = NPCForm()
    placeform = PlaceForm()
    lootform = LootForm()
    playerform = PlayerForm()
    noteform = NoteForm()
    delform = DeleteForm()
    sessionform=SessionForm()

    if request.method == 'POST':
        if gameform.gamesubmit.data:

            game = Games(name=gameform.name.data, imglink=gameform.imglink.data, sessions=gameform.sessions.data, secret=gameform.secret.data, dm_id=gameform.dm_id.data)
            db.session.add(game)
            db.session.commit()
            games = Games.query.all()
        elif userform.usersubmit.data:

            user = Users(name=userform.name.data, email=userform.email.data, realname=userform.realname.data, hash=generate_password_hash(userform.hash.data, method='sha256'))
            db.session.add(user)
            db.session.commit()
            users = Users.query.all()

        elif charform.charsubmit.data:
            char = Characters(name=charform.name.data, imglink=charform.imglink.data, bio=charform.bio.data, platinum=charform.platinum.data, gold=charform.gold.data, silver=charform.silver.data, copper=charform.copper.data, experience=charform.experience.data, strength=charform.strength.data, dexterity=charform.dexterity.data, constitution=charform.constitution.data, wisdom=charform.wisdom.data, intelligence=charform.intelligence.data, charisma=charform.charisma.data, user_id=charform.user_id.data, game_id=charform.game_id.data)
            db.session.add(char)
            db.session.commit()
            characters = Characters.query.all()

        elif npcform.npcsubmit.data:
            npc = NPCs(name=npcform.name.data, secret_name=npcform.secret_name.data, bio=npcform.bio.data, secret_bio=npcform.secret_bio.data, game_id=npcform.game_id.data, place_id=npcform.place_id.data)
            db.session.add(npc)
            db.session.commit()
            npcs = NPCs.query.all()

        elif placeform.placesubmit.data:
            place = Places(name=placeform.name.data, bio=placeform.bio.data, secret_bio=placeform.secret_bio.data, game_id=placeform.game_id.data)
            db.session.add(place)
            db.session.commit()
            places = Places.query.all()

        elif lootform.lootsubmit.data:
            loot = Loot(name=lootform.name.data, bio=lootform.bio.data, copper_value=lootform.copper_value.data, owner_id=lootform.owner_id.data)
            db.session.add(loot)
            db.session.commit()
            loots = Loot.query.all()

        elif noteform.notesubmit.data:
            note = Notes(note=noteform.note.data, private=noteform.private.data, in_character=noteform.in_character.data, session_number=noteform.session_number.data, character=noteform.character.data, game_id=noteform.game_id.data, charname=noteform.charname.data, user_id=noteform.user_id.data)
            db.session.add(note)
            db.session.commit()
            notes = Notes.query.all()

        elif playerform.playersubmit.data:
            player = Players(users_id=playerform.users_id.data, games_id=playerform.games_id.data)
            db.session.add(player)
            db.session.commit()
            players = Players.query.all()

        elif sessionform.sessionsubmit.data:
            session = Sessions(number=sessionform.number.data, title=sessionform.title.data, synopsis=sessionform.synopsis.data, games_id=sessionform.games_id.data)
            db.session.add(session)
            db.session.commit()
            sessions = Sessions.query.all()

    delform.user_group_id.choices = [(g.id) for g in Users.query.order_by('id')]
    delform.game_group_id.choices = [(g.id) for g in Games.query.order_by('id')]
    delform.character_group_id.choices = [(g.id) for g in Characters.query.order_by('id')]
    delform.npc_group_id.choices = [(g.id) for g in NPCs.query.order_by('id')]
    delform.place_group_id.choices = [(g.id) for g in Places.query.order_by('id')]
    delform.loot_group_id.choices = [(g.id) for g in Loot.query.order_by('id')]
    delform.note_group_id.choices = [(g.id) for g in Notes.query.order_by('id')]
    delform.session_group_id.choices = [(g.id) for g in Sessions.query.order_by('id')]
    delform.player_group_id.choices = [(g.id) for g in Players.query.order_by('id')]


    return render_template('test_tables.html',
        uservalues=uservalues,
        userheads = userheads,
        gameheads = gameheads,
        characterheads = characterheads,
        npcheads = npcheads,
        placeheads = placeheads,
        lootheads = lootheads,
        noteheads=noteheads,
        playersheads=playersheads,
        sessionheads=sessionheads,
        users = users,
        games = games,
        players=players,
        characters = characters,
        npcs = npcs,
        places = places,
        loots = loots,
        notes = notes,
        sessions=sessions,
        delform = delform,
        userform = userform,
        gameform = gameform,
        charform=charform,
        npcform=npcform,
        placeform=placeform,
        lootform=lootform,
        noteform=noteform,
        playerform=playerform,
        sessionform=sessionform)

@main.route('/confirming', methods = ['POST'])
@login_required
def post_test_tables():
    delete = DeleteForm()
    if delete.note_group_id.data:
        delete_id = delete.note_group_id.data
        deleted = Notes.query.filter_by(id = delete_id).first()
        db.session.query(Notes).filter(Notes.id==delete_id).delete()
        flash("Note %s: '%s' has been successfully deleted" % (deleted.id, deleted.note))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.session_group_id.data:
        delete_id = delete.session_group_id.data
        deleted = Sessions.query.filter_by(id = delete_id).first()
        db.session.query(Sessions).filter(Sessions.id==delete_id).delete()
        flash("Session %s: '%s' has been successfully deleted" % (deleted.number, deleted.title))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.user_group_id.data:
        delete_id = delete.user_group_id.data
        deleted = Users.query.filter_by(id = delete_id).first()
        db.session.query(Users).filter(Users.id==delete_id).delete()
        flash("User %s: '%s' has been successfully deleted" % (deleted.id, deleted.name))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.game_group_id.data:
        delete_id = delete.game_group_id.data
        deleted = Games.query.filter_by(id = delete_id).first()
        db.session.query(Games).filter(Games.id==delete_id).delete()
        flash("Game %s: '%s' has been successfully deleted" % (deleted.id, deleted.name))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.character_group_id.data:
        delete_id = delete.character_group_id.data
        deleted = Characters.query.filter_by(id = delete_id).first()
        db.session.query(Characters).filter(Characters.id==delete_id).delete()
        flash("Character %s: '%s' has been successfully deleted" % (deleted.id, deleted.name))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.npc_group_id.data:
        delete_id = delete.npc_group_id.data
        deleted = NPCs.query.filter_by(id = delete_id).first()
        db.session.query(NPCs).filter(NPCs.id==delete_id).delete()
        flash("NPC %s: '%s' has been successfully deleted" % (deleted.id, deleted.name))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.place_group_id.data:
        delete_id = delete.place_group_id.data
        deleted = Places.query.filter_by(id = delete_id).first()
        db.session.query(Places).filter(Places.id==delete_id).delete()
        flash("Place %s: '%s' has been successfully deleted" % (deleted.id, deleted.name))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.loot_group_id.data:
        delete_id = delete.loot_group_id.data
        deleted = Loot.query.filter_by(id = delete_id).first()
        db.session.query(Loot).filter(Loot.id==delete_id).delete()
        flash("Loot %s: '%s' has been successfully deleted" % (deleted.id, deleted.name))
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.player_group_id.data:
        delete_id = delete.player_group_id.data
        deleted = Players.query.filter_by(id = delete_id).first()
        db.session.query(Players).filter(Players.id==delete_id).delete()
        flash("Player %s: '%s' has been successfully deleted" % (deleted.id, deleted.users_id))
        db.session.commit()
        return redirect(url_for('main.test_tables'))

@main.route('/confirm', methods = ['POST'])
@login_required
def confirm():
    form = ConForm()
    if session['table_to_edit'] == 'Users':
        row_to_delete = Users.query.filter_by(id = session.get('id_to_delete')).first()
    elif session['table_to_edit'] == 'Games':
        row_to_delete = Games.query.filter_by(id = session.get('id_to_delete')).first()
    elif session['table_to_edit'] == 'Characters':
        row_to_delete = Characters.query.filter_by(id = session.get('id_to_delete')).first()
    elif session['table_to_edit'] == 'NPCs':
        row_to_delete = NPCs.query.filter_by(id = session.get('id_to_delete')).first()
    elif session['table_to_edit'] == 'Places':
        row_to_delete = Places.query.filter_by(id = session.get('id_to_delete')).first()
    elif session['table_to_edit'] == 'Loot':
        row_to_delete = Loot.query.filter_by(id = session.get('id_to_delete')).first()

    # if the cancel button is pressed
    if form.cancel.data:
        return redirect(url_for('main.test_tables'))
    # if data is submitted correctly and matches
    elif form.todelete.data == row_to_delete.name:
        # delete user
        flash("%s has been successfully deleted" % session['name_to_delete'])
        db.session.delete(row_to_delete)
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    # if data is entered incorrectly
    else:
        form = ConForm()
        flash("names do not match, check to make sure you are deleting the correct thing")
        return render_template('confirm.html',
            form = form,
            name = session['name_to_delete'])

@main.route("/test")
def test():
    return "sup bra"

@main.route('/nuked', methods=["GET"])
@login_required
def nuked():
    nuke()
    return "nuked"
