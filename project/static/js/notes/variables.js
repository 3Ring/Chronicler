/*
global variables
*/
const SOCKET = set_socket();
const USER_IS_DM = set_dm_user();
const CLASSNAME_HIDDEN = "hidden";
const CLASSNAME_ACTIVE = "--active";
const CLASSNAME_ACTIVE_SESSIONLIST = "current";
let CURRENT_SESSION_NUMBER = 0;

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
