from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug import datastructures
from werkzeug.security import generate_password_hash

from .events import *
from .classes import *
from flask_login import login_required, current_user
from . import db
from .helpers import validate
import json

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
        dm_games=Games.query.filter_by(dm_id=current_user.id).all()
        
        return render_template("index.html",
            games=games,
            dm_games=dm_games)

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

@main.route('/create', methods=["GET", "POST"])
@login_required
def create():
    gameform=GameForm()
    if request.method=="GET":
        return render_template('create.html',
            gameform=gameform)
    else:
        game=Games(name=gameform.name.data, dm_id=current_user.id, imglink=gameform.imglink.data, sessions=gameform.sessions.data, published=gameform.published.data)
        db.session.add(game)
        db.session.flush()
        id=game.id
        db.session.commit()
        return redirect(url_for('main.notes', id=id))

@main.route('/notes/<id>', methods = ['GET'])
@login_required
def notes(id):


    # figure out how many sessions there are and if they have any notes attached to them
    session_titles=Sessions.query.filter_by(games_id=id).all()
    dmid=Games.query.with_entities(Games.dm_id).filter_by(id=id).first()[0]
    logs = []
    if session_titles != None:
        # query the notes and organize them by session in reverse order
        for i in range(session_titles[-1].number):
            if i == 0:
                j=session_titles[0].number
            if i == (session_titles[j-1].number-1):
                logs.append(Notes.query.filter_by(game_id=id).filter_by(session_id=(i+1)).all())
                j+=1
            else:
                logs.append('No Session data')
        session_titles.reverse()
        for log in logs:
            try:
                if len(log) > 1:
                    log.reverse()
            except:
                continue

    
    return render_template('notes.html',
        logs=logs,
        id=id,
        session_titles=session_titles,
        dmid=dmid)

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
    uservalues=Users().values
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
    sessionheads=Sessions().head
    sessions=Sessions.query.all()
    test=Test.query.all()


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
            note = Notes(note=noteform.note.data, private=noteform.private.data, in_character=noteform.in_character.data, session_id=noteform.session.data, character=noteform.character.data, game_id=noteform.game.data)
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


    for user in users:
        print('\n\n\n\n', user)
    return render_template('test_tables.html',
        uservalues=uservalues,
        userheads = userheads,
        gameheads = gameheads,
        charheads = charheads,
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
        sessionform=sessionform,
        test=test)

@main.route('/confirming', methods = ['POST'])
@login_required
def post_test_tables():
    delete = DeleteForm()
    if delete.note_group_id.data:
        delete_id = delete.note_group_id.data
        deleted = Notes.query.filter_by(id = delete_id).first()
        flash("Note %s: '%s' has been successfully deleted" % (deleted.id, deleted.note))
        db.session.delete(deleted)
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    elif delete.session_group_id.data:
        delete_id = delete.session_group_id.data
        deleted = Sessions.query.filter_by(id = delete_id).first()
        flash("Session %s: '%s' has been successfully deleted" % (deleted.number, deleted.title))
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


@main.route('/test', methods = ['GET'])
def test():
    testform = TestForm()
    tests=Test.query.all()
    array=[]
    for test in tests:
        array.append(test)
    array.reverse()
    return render_template('test.html', testform=testform, tests=array)

