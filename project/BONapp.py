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
        games=Games.query.filter(
            Games.id.in_(
                Players.query.with_entities(Players.games_id).
                    filter(Players.users_id.in_(
                        Users.query.with_entities(
                            Users.id).filter_by(
                                id=current_user.id)))))
        
        return render_template("index.html", games=games)

    return render_template("index.html")

@main.route('/join/<int:id>', methods = ['POST', 'GET'])
@login_required
def join(id):
    if id == 0:
        games=Games.query.all()
        return render_template("join.html",
        games=games)
    else:
        return redirect(url_for('main.joining', id=id))


@main.route('/joining/<int:id>', methods = ['GET', 'POST'])
@login_required
def joining(id):
    
    charform=CharForm()
    game=Games.query.filter_by(id=id).first()
    if request.method=='GET':
        return render_template('joining.html',
            charform=charform,
            game=game)
    if charform.charsubmit.data:
        character=Characters(name=charform.name.data, imglink=charform.imglink.data, bio=charform.bio.data, user_id=current_user.id, game_id=id)
        db.session.add(character)
        db.session.commit()
        flash("{0} has joined the {1}!!".format(charform.name.data, game.name), "alert-success")
        return redirect(url_for('main.index'))

@main.route('/create')
@login_required
def create():
    gameform=GameForm()
    render_template('create.html',
        gameform=gameform)

@main.route('/notes/<id>', methods = ['POST', 'GET'])
@login_required
def notes(id):

    # figure out how many sessions there are and if they have any notes attached to them
    form = NoteForm()
    sessions = Notes.query.with_entities(Notes.session_id).filter_by(game_id=id).distinct()
    session_ints = []
    logs = []
    for session in sessions:
        session_ints.append(int(str(session)[1]))
    # query the notes and organize them by session
    for i in range(session_ints[-1]):
        if i == 0:
            j=0
        if i == (session_ints[j]-1):
            logs.append(Notes.query.filter_by(game_id=id).filter_by(session_id=(i+1)).all())
            j+=1
        else:
            logs.append('No Session data')
    session_ints.reverse()

    if request.method == 'POST':
    
        character=Characters.query.with_entities(Characters.id).filter_by(user_id=current_user.id, game_id=id).first()
        print('\n\n\n\n', character[0], '\n\n\n\n')
        charname=Characters.query.with_entities(Characters.name).filter_by(id=character[0])
        note = Notes(note=form.note.data, session_id=form.session.data, private=form.private.data, in_character=form.in_character.data, character=character[0], charname=charname, game_id=id)
        db.session.add(note)
        db.session.commit()
        sessions = Notes.query.with_entities(Notes.session_id).filter_by(game_id=id).distinct()
        session_ints = []
        logs = []
        for session in sessions:
            session_ints.append(int(str(session)[1]))
        # query the notes and organize them by session
        for i in range(session_ints[-1]):
            if i == 0:
                j=0
            if i == (session_ints[j]-1):
                logs.append(Notes.query.filter_by(game_id=id).filter_by(session_id=(i+1)).all())
                j+=1
            else:
                logs.append('No Session data')
        session_ints.reverse()
        return render_template('notes.html',
            logs=logs,
            noteform=form,
            id=id,
            session_ints=session_ints)
    else:
        return render_template('notes.html',
            logs=logs,
            noteform=form,
            id=id,
            session_ints=session_ints)

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


