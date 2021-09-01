

document.addEventListener("DOMContentLoaded", function(event) { 
  (function() {

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//
// H E L P E R    F U N C T I O N S
//
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

/**
 * Function to check if we clicked inside an element with a particular class
 * name.
 * 
 * @param {Object} e The event
 * @param {String} className The class name to check against
 * @return {Boolean}
 */
function clickInsideElement( e, className ) {
  var el = e.srcElement || e.target;
  
  if ( el.classList.contains(className) ) {
    return el;
  } else {
    while ( el = el.parentNode ) {
      if ( el.classList && el.classList.contains(className) ) {
        return el;
      }
    }
  }

  return false;
}

/**
 * Get's exact position of event.
 * 
 * @param {Object} e The event passed in
 * @return {Object} Returns the x and y position
 */
function getPosition(e) {
  var posx = 0;
  var posy = 0;

  if (!e) var e = window.event;
  
  if (e.pageX || e.pageY) {
    posx = e.pageX;
    posy = e.pageY;
  } else if (e.clientX || e.clientY) {
    posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
    posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
  }

  return {
    x: posx,
    y: posy
  }
}

function edit_note_func(note_id) {
    let text = document.getElementById("input_change_" + note_id).value;
    let game_id = document.getElementById('note_game_id');
    let user_id = document.getElementById('note_user_id');
    socket.emit("edit_note", text, game_id, user_id, note_id);
};
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//
// C O R E    F U N C T I O N S
//
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

/**
 * Variables.
 */


var contextMenuClassName = "note_edit_menu";
var menuState = 0;
var contextMenuItemClassName = "note_edit_menu_item";
var contextMenuLinkClassName = "note_edit_menu_link";
var contextMenuActive = "note_edit_menu--active";

var taskItemClassName = "note_edit_button";
var taskItemInContext;

var clickCoords;
var clickCoordsX;
var clickCoordsY;

var menu = document.querySelector("#note_edit_menu");
var menuItems = menu.querySelectorAll(".note_edit_menu_item");
var menuState = 0;
var menuWidth;
var menuHeight;
var menuPosition;
var menuPositionX;
var menuPositionY;

var windowWidth;
var windowHeight;

/**
 * Initialise our application's code.
 */
function init() {
  contextListener();
  clickListener();
  keyupListener();
  resizeListener();
}

/**
 * Listens for contextmenu events.
 */
function contextListener() {
  document.addEventListener( "contextmenu", function(e) {
    taskItemInContext = clickInsideElement( e, taskItemClassName );

    if ( taskItemInContext ) {
      e.preventDefault();
      toggleMenuOn();
      positionMenu(e);
    } else {
      taskItemInContext = null;
      toggleMenuOff();
    }
  });
}

/**
 * Listens for click events.
 */
function clickListener() {
  document.addEventListener( "click", function(e) {
    var clickeElIsLink = clickInsideElement( e, contextMenuLinkClassName );

    if ( clickeElIsLink ) {
      e.preventDefault();
      menuItemListener( clickeElIsLink );
    } else {
      var button = e.which || e.button;
      if ( button === 1 ) {
        toggleMenuOff();
      }
    }
  });
}

/**
 * Listens for keyup events.
 */
function keyupListener() {
  window.onkeyup = function(e) {
    if ( e.keyCode === 27 ) {
      toggleMenuOff();
    }
  }
}

/**
 * Window resize event listener
 */
function resizeListener() {
  window.onresize = function(e) {
    toggleMenuOff();
  };
}

/**
 * Turns the custom context menu on.
 */
function toggleMenuOn() {
  if ( menuState !== 1 ) {
    menuState = 1;
    menu.classList.add( contextMenuActive );
  }
}

/**
 * Turns the custom context menu off.
 */
function toggleMenuOff() {
  if ( menuState !== 0 ) {
    menuState = 0;
    menu.classList.remove( contextMenuActive );
  }
}

/**
 * Positions the menu properly.
 * 
 * @param {Object} e The event
 */
function positionMenu(e) {
  clickCoords = getPosition(e);
  clickCoordsX = clickCoords.x;
  clickCoordsY = clickCoords.y;

  menuWidth = menu.offsetWidth + 4;
  menuHeight = menu.offsetHeight + 4;

  windowWidth = window.innerWidth;
  windowHeight = window.innerHeight;

  if ( (windowWidth - clickCoordsX) < menuWidth ) {
    menu.style.left = windowWidth - menuWidth + "px";
  } else {
    menu.style.left = clickCoordsX + "px";
  }

  if ( (windowHeight - clickCoordsY) < menuHeight ) {
    menu.style.top = windowHeight - menuHeight + "px";
  } else {
    menu.style.top = clickCoordsY + "px";
  }
}
/**
 * creates the listener for the edit form once it has been
 */
// document.addEventListener('edit_button_build', function (e) {
//   var note_id = e.detail;
//   console.log("event", note_id);
//   document.getElementById("form_" + note_id).onsubmit = function(note_id) {
//     console.log("submitted");
//     let text = document.getElementById("input_change_" + note_id).value;
//     let game_id = document.getElementById('note_game_id');
//     let user_id = document.getElementById('note_user_id');
//     socket.emit("edit_note", text, game_id, user_id, note_id);
//   }
// });

/**
 * Dummy action function that logs an action when a menu item link is clicked
 * 
 * @param {HTMLElement} link The link that was clicked
 */
function menuItemListener( link ) {
  console.log( "Task ID - " + taskItemInContext.getAttribute("data-id") + ", Task action - " + link.getAttribute("data-action"));
  el_id = taskItemInContext.getAttribute("data-id");
  let keys = ["id", "private", "in_character"];
  let note_meta = {}
  let long = 0
  for (let i = 0, j = 0; i < el_id.length; i++) {
    if (el_id[i] === "_") 
    {
      long = 0
    } else {
      if (long == 0) {
        note_meta[keys[j]] = el_id[i];
        long = 1
        j++;
      } else {
        j--;
        note_meta[keys[j]] += el_id[i];
        j++;
      }
    }
  }

  if (link.getAttribute("data-action") == "edit") {
    var note_id = note_meta.id;
    var is_private = note_meta.private;
    var is_in_character = note_meta.in_character;
    var inner = document.getElementById("inner_" + note_id);
    var innertext = inner.innerHTML;
    inner.innerHTML = "<form onsubmit='edit_note_func(" + note_id + ")' id='form_" + note_id + "'><input type='text' value='" + innertext + "' id='input_change_" + note_id + "'><label for='change_private'>Make Private?</label><input type='checkbox' id='change_private' value='" + is_private + "'><label for='make_in_character'>Change to <i>in character?</i></label><input type='checkbox' id='make_in_character' value='" + is_in_character + "'><input type='submit' value='submit' id='change_submit_" + note_id + "'></form>";
  }
  toggleMenuOff();
}

/**
 * Run the app.
 */
init();

})();
});