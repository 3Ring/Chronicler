const SOCKET = set_socket();
/**
 * Create a client side socket connection
 * @returns The socket object.
 */
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