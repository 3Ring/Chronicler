const socket = io();



document.addEventListener("DOMContentLoaded", function(event) {
	const evt = new Event("NewSessionFormCreated", {
		"bubbles": true, "cancelable": false
	});
	var session_form_deployed = false;
	var note_is_private = false;
	var note_is_in_character = false;

	// display new session card
	socket.on('fill_new_session', function(new_card, number) {
		session_cards = document.getElementById('Session Cards');
		session_cards.insertAdjacentHTML('afterbegin', new_card);
	});


	// display new note
	socket.on('fill_new_note', function(new_note, priv, session_number, in_character) {
		this_session = document.getElementById('session_card_' + session_number);
		this_session.insertAdjacentHTML('afterbegin', new_note);
	});

	// set the values of the checkboxes based on whether they are checked or not
	document.getElementById('note_in_character').onclick = function() {
		if (note_is_in_character) {
			document.getElementById('note_in_character').value = 'n';
			note_is_in_character = false;
		} else {
			document.getElementById('note_in_character').value = 'y';
			note_is_in_character = true;
		}
	};
	document.getElementById('note_private').onclick = function() {
		if (note_is_private) {
			document.getElementById('note_private').value = 'n';
			note_is_private = false;
		} else {
			document.getElementById('note_private').value = 'y';
			note_is_private = true;
		}
	};






	// create form for making new session card
	document.getElementById("new_session_button").onclick = function() {
		// If new session form has already been deployed then pushing the button again will close it
		if (session_form_deployed) {
			document.getElementById("new_session_form_div").innerHTML = "";
			session_form_deployed = false;
		} else {
			// Create and deploy new session form
			document.getElementById("new_session_form_div").innerHTML = "<h2>Session Info</h2><form id ='new_session_form'><input id='new_session_form_id' type='hidden' value='{{id}}'><input id='new_session_form_number' required, placeholder='Number(Required)' type='number' min=0><input id='new_session_form_title' required, placeholder='Title(Required)' type='text'><input id='new_session_form_synopsis' type='text', placeholder='Optional Synopsis'><input type='submit' value ='Make Session'></input><input type='button' id='cancel_new_session' value='Cancel'></input></form>";
			var new_session_form_id = document.getElementById('new_session_form_id'),
				new_session_form_number = document.getElementById('new_session_form_number'),
				new_session_form_title = document.getElementById('new_session_form_title'),
				new_session_form_synopsis = document.getElementById('new_session_form_synopsis');
			document.dispatchEvent(evt);
			session_form_deployed = true;
		}
	};



	// capture and send new note to server
	document.getElementById("note_form").onsubmit = function() {
		var new_note_user_id = document.getElementById('note_user_id'),
			new_note_note = document.getElementById('note_note'),
			new_note_private = document.getElementById('note_private'),
			new_note_in_character = document.getElementById('note_in_character'),
			new_note_game_id = document.getElementById('note_game_id');

		socket.emit('send_new_note', new_note_user_id.value, new_note_game_id.value, new_note_note.value, new_note_private.value, new_note_in_character.value);
		return false;
	};

});
// Create on sumbit function for new session card after form for it has been created
document.addEventListener("NewSessionFormCreated", function(event) {
	// cancel button function
	document.getElementById("cancel_new_session").addEventListener("click", function() {
		document.getElementById('new_session_form_div').innerHTML = '';
		session_form_deployed = false;
	});
	// capture and send new session to server
	document.getElementById('new_session_form').onsubmit = function() {
		// ensure that form is filled out correctly
		if (new_session_form_id.value !== '' && new_session_form_number.value !== '' && new_session_form_title.value !== '' && parseInt(new_session_form_number.value) > -1) {
			if (document.getElementById("session_card_" + new_session_form_number.value) === null) {
				socket.emit('send_new_session', new_session_form_id.value, new_session_form_number.value, new_session_form_title.value, new_session_form_synopsis.value);
				document.getElementById("new_session_form_div").innerHTML = "";
				session_form_deployed = false;
				return false;
			} else {
				alert("Session number must be unique");
				return false;
			}
		} else {
			alert("Must fill out required fields");
			return false;
		}

	};
});