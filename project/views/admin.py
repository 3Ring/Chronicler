

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

            user = Users(name=userform.name.data, email=userform.email.data, realname=userform.realname.data, hash=generate_password_hash(userform.password.data, method='sha256'))
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