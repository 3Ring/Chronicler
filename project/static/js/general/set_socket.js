const SOCKET = set_socket();
function set_socket() {
  let socket;
  if (heroku) {
    socket = io("https://www.chronicler.gg", {
      withCredentials: true,
    });
  } else {
    socket = io();
  }
  return socket;
}