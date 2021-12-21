/*
global variables
*/
const socket = set_socket();
const user_is_dm = set_dm_user();
const className__hidden = "hidden";
const className__active = "--active";
const className__active_sessionList = "current";
var current__session_number = 0;

/*
Set variable functions
*/
function set_dm_user() {
  let dm = false;
  if (user_id == dm_id) {
    dm = true;
  }
  return dm;
}
function set_socket() {
  let socket = null;
  if (heroku) {
    socket = io("https://www.chronicler.gg", {
      withCredentials: true,
    });
  } else {
    socket = io();
  }
  return socket;
}
