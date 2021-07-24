from flask import Blueprint, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import generate_password_hash

from .classes import *
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        # test=Users.query.filter_by(email='zack@zack.com')
        # test=Games.query.filter_by(id=1)
        # stepone=Users.query.filter_by(id=current_user.id)
        # test=Players.query.(users_id=stepone)
        # test=Games.query.filter(Games.id.in_(Players.query.filter(Users.id.in_(Users.query.with_entities(Users.id).filter_by(id=current_user.id))))).all()
        games=Games.query.filter(
            Games.id.in_(
                Players.query.with_entities(Players.games_id).
                    filter(Players.users_id.in_(
                        Users.query.with_entities(
                            Users.id).filter_by(
                                id=current_user.id)))))
        


        # SELECT * FROM games WHERE id IN(SELECT games_id FROM players WHERE users_id IN(SELECT id FROM users WHERE id LIKE '%1%'))
        # test=Games.query.filter_by(id=1)
        # games=Games.query.filter_by(id=Players.query.filter_by(games_id=1))
        return render_template("index.html", games=games)

    return render_template("index.html")

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/test_tables', methods = ['GET', 'POST'])
@login_required
def test_tables():

    # make sure that only the admin can access this site
    if not current_user.id == 1:
        return redirect(url_for('main.profile'))
    
    # set variable so Flask can build the site
    userheads = Users().head
    users = Users.query.all()
    gameheads = Games().head
    games = Games.query.all()
    charheads = Characters().head
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


    userform = UserForm()
    gameform = GameForm()
    charform = CharForm()
    npcform = NPCForm()
    placeform = PlaceForm()
    lootform = LootForm()
    playerform = PlayerForm()
    noteform = NoteForm()
    delform = DeleteForm()

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
            note = Notes(note=noteform.note.data, private=noteform.private.data, in_character=noteform.in_character.data, session_id=noteform.session.data, character=noteform.character.data, game_id=noteform.game.data)
            db.session.add(note)
            db.session.commit()
            notes = Notes.query.all()

        elif playerform.playersubmit.data:
            player = Players(users_id=playerform.users_id.data, games_id=playerform.games_id.data)
            db.session.add(player)
            db.session.commit()
            players = Players.query.all()

    delform.user_group_id.choices = [(g.id) for g in Users.query.order_by('id')]
    delform.game_group_id.choices = [(g.id) for g in Games.query.order_by('id')]
    delform.character_group_id.choices = [(g.id) for g in Characters.query.order_by('id')]
    delform.npc_group_id.choices = [(g.id) for g in NPCs.query.order_by('id')]
    delform.place_group_id.choices = [(g.id) for g in Places.query.order_by('id')]
    delform.loot_group_id.choices = [(g.id) for g in Loot.query.order_by('id')]
    delform.note_group_id.choices = [(g.id) for g in Notes.query.order_by('id')]

    return render_template('test_tables.html',
        userheads = userheads,
        gameheads = gameheads,
        charheads = charheads,
        npcheads = npcheads,
        placeheads = placeheads,
        lootheads = lootheads,
        noteheads=noteheads,
        users = users,
        games = games,
        players=players,
        characters = characters,
        npcs = npcs,
        places = places,
        loots = loots,
        notes = notes,
        delform = delform,
        userform = userform,
        gameform = gameform,
        charform=charform,
        npcform=npcform,
        placeform=placeform,
        lootform=lootform,
        noteform=noteform,
        playerform=playerform,
        playersheads=playersheads)

@main.route('/confirming', methods = ['POST'])
@login_required
def post_test_tables():
    delete = DeleteForm()
    if delete.note_group_id.data:
        delete_id = delete.note_group_id.data
        deleted = Notes.query.filter_by(id = delete_id).first()
        flash("%s has been successfully deleted" % session['name_to_delete'])
        db.session.delete(deleted)
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.user_group_id.data:
        delete_id = delete.user_group_id.data
        deleted = Users.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Users'
    elif delete.game_group_id.data:
        delete_id = delete.game_group_id.data
        deleted = Games.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Games'
    elif delete.character_group_id.data:
        delete_id = delete.character_group_id.data
        deleted = Characters.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Characters'
    elif delete.npc_group_id.data:
        delete_id = delete.npc_group_id.data
        deleted = NPCs.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'NPCs'
    elif delete.place_group_id.data:
        delete_id = delete.place_group_id.data
        deleted = Places.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Places'
    elif delete.loot_group_id.data:
        delete_id = delete.loot_group_id.data
        deleted = Loot.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Loot'
    session['name_to_delete'] = deleted.name
    session['id_to_delete'] = delete_id
    flash("Are you sure you want to delete %s?" % session['name_to_delete'])
    form = ConForm()
    return render_template('confirm.html',
    form = form,
    name = session['name_to_delete'])

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

@main.route('/notes/<id>', methods = ['POST', 'GET'])
@login_required
def notes(id):
    # this needs to be changed to be dynamic (todo)
    form = NoteForm()
    log = Notes.query.filter_by(game_id=id).order_by(Notes.session_id.desc(), Notes.date_added.desc())
    if request.method == 'POST':
        note = Notes(note=form.note.data, session_id=form.session.data, private=form.private.data, in_character=form.in_character.data, character=form.character.data, game_id=form.game.data)
        db.session.add(note)
        db.session.commit()
        log = Notes.query.filter_by(game_id=id).order_by(Notes.session_id.desc(), Notes.date_added.desc())
        return render_template('notes.html',
            log=log,
            noteform=form,
            id=id)
    else:

        return render_template('notes.html',
            log=log,
            noteform=form,
            id=id)
